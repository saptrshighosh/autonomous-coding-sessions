#!/usr/bin/env python3
"""Audit a project's Claude Code setup for unattended use.

Deterministic, standard-library only, read-only. It never modifies the project.

Usage:
    audit_setup.py [PROJECT_DIR] [--json] [--fail-on {high,medium,low,none}]

Every finding is a heuristic over files on disk. A finding means "look at this",
not "this is wrong". The setting names checked here (permissions.deny,
permissions.defaultMode, hooks) follow the Claude Code settings format, but
confirm them against the current docs.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

SEVERITIES = ("high", "medium", "low", "info")
EMPHASIS_RE = re.compile(
    r"\b(IMPORTANT|CRITICAL|NEVER|ALWAYS|MUST|DO NOT|DON'T FORGET|YOU MUST)\b"
)
LONG_CLAUDE_MD_LINES = 150  # heuristic threshold, ours, not from any source
BLOCKING_EVENTS = ("Stop", "TaskCompleted", "PostToolUse", "SubagentStop")
SCRIPT_TOKEN_RE = re.compile(r"[^\s\"']+\.(?:sh|bash|py)\b")


def finding(fid, severity, message, fix, where=""):
    assert severity in SEVERITIES
    return {"id": fid, "severity": severity, "where": where, "message": message, "fix": fix}


def load_json(path: Path, findings: list):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        findings.append(
            finding(
                "SETTINGS_INVALID_JSON",
                "high",
                f"{path.name} is not valid JSON ({exc.msg}, line {exc.lineno}).",
                "Fix the JSON; Claude Code cannot apply a settings file it cannot parse.",
                str(path),
            )
        )
    except OSError as exc:
        findings.append(finding("SETTINGS_UNREADABLE", "low", str(exc), "Check permissions.", str(path)))
    return None


def check_claude_md(root: Path, findings: list):
    path = root / "CLAUDE.md"
    if not path.is_file():
        findings.append(
            finding(
                "CLAUDE_MD_MISSING",
                "info",
                "No CLAUDE.md found. That is fine if there is nothing invisible in the code to record.",
                "Add one only for facts Claude cannot learn from the repo.",
            )
        )
        return
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    hits = []
    for number, line in enumerate(lines, 1):
        if EMPHASIS_RE.search(line):
            hits.append((number, line.strip()))
    if hits:
        sample = "; ".join(f"L{n}: {text[:60]}" for n, text in hits[:5])
        findings.append(
            finding(
                "CLAUDE_MD_EMPHASIS",
                "medium",
                f"{len(hits)} line(s) use shouted emphasis words (e.g. IMPORTANT, NEVER). {sample}",
                "Rewrite plainly or delete. Hard limits belong in deny rules, not in CLAUDE.md.",
                str(path),
            )
        )
    if len(lines) > LONG_CLAUDE_MD_LINES:
        findings.append(
            finding(
                "CLAUDE_MD_LONG",
                "low",
                f"CLAUDE.md is {len(lines)} lines (heuristic threshold {LONG_CLAUDE_MD_LINES}).",
                "Keep only what Claude cannot see in the code.",
                str(path),
            )
        )


def collect_deny_rules(settings_list):
    rules = []
    for settings in settings_list:
        perms = settings.get("permissions") if isinstance(settings, dict) else None
        if isinstance(perms, dict) and isinstance(perms.get("deny"), list):
            rules.extend(str(r) for r in perms["deny"])
    return rules


def iter_hook_commands(settings):
    hooks = settings.get("hooks") if isinstance(settings, dict) else None
    if not isinstance(hooks, dict):
        return
    for event, groups in hooks.items():
        if not isinstance(groups, list):
            continue
        for group in groups:
            for handler in (group or {}).get("hooks", []) if isinstance(group, dict) else []:
                if isinstance(handler, dict) and handler.get("type", "command") == "command":
                    command = handler.get("command")
                    if isinstance(command, str):
                        yield event, command


def resolve_script(token: str, root: Path):
    cleaned = token.replace("$CLAUDE_PROJECT_DIR", str(root)).replace("${CLAUDE_PROJECT_DIR}", str(root))
    candidate = Path(cleaned)
    if not candidate.is_absolute():
        candidate = root / candidate
    return candidate if candidate.is_file() else None


def check_settings(root: Path, findings: list):
    files = [root / ".claude" / "settings.json", root / ".claude" / "settings.local.json"]
    loaded = []
    for path in files:
        if path.is_file():
            data = load_json(path, findings)
            if data is not None:
                loaded.append((path, data))
    if not loaded:
        findings.append(
            finding(
                "NO_PROJECT_SETTINGS",
                "medium",
                "No .claude/settings.json found, so no project-level deny rules or hooks are committed.",
                "Add deny rules for irreversible actions and commit them (see templates/deny-rules.settings.json).",
            )
        )
        return

    datas = [d for _, d in loaded]

    for path, data in loaded:
        perms = data.get("permissions") if isinstance(data, dict) else None
        if isinstance(perms, dict) and perms.get("defaultMode") == "bypassPermissions":
            findings.append(
                finding(
                    "BYPASS_PERMISSIONS",
                    "high",
                    "permissions.defaultMode is bypassPermissions, which skips permission checks.",
                    "Prefer auto mode plus deny rules; bypass removes the classifier and the approvals.",
                    str(path),
                )
            )

    rules = collect_deny_rules(datas)
    if not rules:
        findings.append(
            finding(
                "NO_DENY_RULES",
                "medium",
                "No permissions.deny rules found.",
                "Add rules for actions you cannot take back (reading secrets, discarding uncommitted work).",
            )
        )
    else:
        if not any(".env" in r for r in rules):
            findings.append(
                finding(
                    "NO_ENV_DENY",
                    "medium",
                    "No deny rule mentions .env.",
                    "Add a deny rule for .env files so a secret cannot land in the transcript.",
                )
            )
        if not any(".ssh" in r for r in rules):
            findings.append(
                finding(
                    "NO_SSH_DENY",
                    "low",
                    "No deny rule mentions .ssh. A sandbox can still read most of the machine by default.",
                    "Add a rule for SSH keys, or run in a cloud session where they do not exist.",
                )
            )

    if not any(isinstance(d, dict) and "sandbox" in d for d in datas):
        findings.append(
            finding(
                "NO_SANDBOX_KEY",
                "info",
                "No sandbox block in project settings. It may be configured elsewhere (user settings or cloud).",
                "Consider a sandbox locally, or a cloud session for long unattended runs.",
            )
        )

    events = set()
    for path, data in loaded:
        for event, command in iter_hook_commands(data):
            events.add(event)
            if event not in BLOCKING_EVENTS:
                continue
            for token in SCRIPT_TOKEN_RE.findall(command):
                script = resolve_script(token, root)
                if script is None:
                    continue
                text = script.read_text(encoding="utf-8", errors="replace")
                if re.search(r"\bexit\s+1\b", text) and not re.search(r"\bexit\s+2\b", text):
                    findings.append(
                        finding(
                            "HOOK_EXIT_1",
                            "medium",
                            f"{script.name} (event {event}) exits 1 on failure and never exits 2.",
                            "A failing check should exit 2 to send Claude back to fix it; exit 1 lets the task complete.",
                            str(script),
                        )
                    )
    if not events & {"Stop", "TaskCompleted"}:
        findings.append(
            finding(
                "NO_VERIFICATION_HOOK",
                "low",
                "No Stop or TaskCompleted hook found, so nothing guarantees checks run before Claude finishes.",
                "Add pass/fail checks as hooks for anything that must run (scripts/hooks/ has examples).",
            )
        )


def check_ci_and_gitignore(root: Path, findings: list):
    ci_markers = [
        root / ".github" / "workflows",
        root / ".gitlab-ci.yml",
        root / ".circleci",
        root / "Jenkinsfile",
        root / "azure-pipelines.yml",
    ]
    if not any(p.exists() for p in ci_markers):
        findings.append(
            finding(
                "NO_CI",
                "medium",
                "No CI configuration detected. CI is the backstop that checks every session's PR the same way.",
                "Add CI that covers the behavior you care about before running sessions in parallel.",
            )
        )
    gitignore = root / ".gitignore"
    text = gitignore.read_text(encoding="utf-8", errors="replace") if gitignore.is_file() else ""
    if (root / ".env").exists() and ".env" not in text:
        findings.append(
            finding(
                "ENV_NOT_IGNORED",
                "medium",
                ".env exists but is not listed in .gitignore.",
                "Ignore it so it never reaches git or a cloud session's repo copy.",
                str(gitignore),
            )
        )


def audit(root: Path):
    findings: list = []
    check_claude_md(root, findings)
    check_settings(root, findings)
    check_ci_and_gitignore(root, findings)
    order = {s: i for i, s in enumerate(SEVERITIES)}
    findings.sort(key=lambda f: (order[f["severity"]], f["id"]))
    return findings


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("project", nargs="?", default=".", help="project directory (default: .)")
    parser.add_argument("--json", action="store_true", help="emit JSON")
    parser.add_argument(
        "--fail-on",
        choices=["high", "medium", "low", "none"],
        default="none",
        help="exit 1 if any finding at or above this severity (default: never)",
    )
    args = parser.parse_args(argv)
    root = Path(args.project).resolve()
    if not root.is_dir():
        print(f"error: {root} is not a directory", file=sys.stderr)
        return 2
    findings = audit(root)

    if args.json:
        print(json.dumps({"project": str(root), "findings": findings}, indent=2))
    else:
        print(f"Audit of {root}")
        if not findings:
            print("No findings.")
        for f in findings:
            where = f" [{f['where']}]" if f["where"] else ""
            print(f"- {f['severity'].upper():6} {f['id']}{where}\n    {f['message']}\n    fix: {f['fix']}")
        print("\nThese are heuristics over files on disk. Review each before acting on it.")

    if args.fail_on != "none":
        limit = SEVERITIES.index(args.fail_on)
        if any(SEVERITIES.index(f["severity"]) <= limit for f in findings):
            return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
