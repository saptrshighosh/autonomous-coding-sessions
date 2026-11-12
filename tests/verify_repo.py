#!/usr/bin/env python3
"""Repository verification: structure, metadata, links, scripts, and honesty checks.

Standard library only. Prints every failure, then exits 1 if there were any.

    python3 tests/verify_repo.py
"""
from __future__ import annotations

import filecmp
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"
MAIN_SKILL = "autonomous-coding-sessions"
EXPECTED_SKILLS = {MAIN_SKILL, "autonomy-audit", "reversibility-check", "verification-plan"}
EXPECTED_AGENTS = {"autonomy-auditor.md", "fresh-context-reviewer.md"}
REQUIRED_ROOT_FILES = [
    "README.md", "INSTALL.md", "CLAUDE.md", "AGENTS.md", "GEMINI.md", "CONTRIBUTING.md",
    "CODE_OF_CONDUCT.md", "SECURITY.md", "TRADEMARKS.md", "NOTICE", "LICENSE", "CHANGELOG.md",
    "Makefile", "install.sh", "gemini-extension.json", "CHECKSUMS.sha256",
    ".gitignore", ".gitattributes", ".editorconfig",
    ".claude-plugin/plugin.json", ".claude-plugin/marketplace.json",
    "docs/README.md", "docs/HONEST-LIMITS.md", "docs/PROVENANCE.md",
    "scripts/package_skill.py", "scripts/gen_checksums.py", "evals/README.md",
]
NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
EVAL_PROMPT_KEYS = {"tags", "max_turns", "timeout_seconds", "allowed_tools"}

failures: list[str] = []


def fail(message: str) -> None:
    failures.append(message)


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def parse_frontmatter(path: Path):
    """Return (dict, body). Handles simple `key: value` lines only."""
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return None, text
    end = text.find("\n---", 4)
    if end == -1:
        return None, text
    block = text[4:end]
    data = {}
    for line in block.splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if ": " in line:
            key, value = line.split(": ", 1)
        elif line.endswith(":"):
            key, value = line[:-1], ""
        else:
            fail(f"{rel(path)}: unparseable frontmatter line {line!r}")
            continue
        data[key.strip()] = value.strip()
    return data, text[end + 4:]


def read_json(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001
        fail(f"{rel(path)}: invalid JSON ({exc})")
        return None


# ---------------------------------------------------------------- structure
def check_required_files():
    for name in REQUIRED_ROOT_FILES:
        if not (ROOT / name).is_file():
            fail(f"missing required file: {name}")


def check_json_files():
    for path in ROOT.rglob("*.json"):
        if ".git" in path.parts:
            continue
        read_json(path)


def check_manifests():
    plugin = read_json(ROOT / ".claude-plugin/plugin.json") or {}
    market = read_json(ROOT / ".claude-plugin/marketplace.json") or {}
    gemini = read_json(ROOT / "gemini-extension.json") or {}
    # Auto-discovery: explicit agents/skills keys can break loading or hide files.
    for key in ("agents", "skills"):
        if key in plugin:
            fail(f"plugin.json must not set '{key}': default auto-discovery is used")
    name = plugin.get("name", "")
    if not NAME_RE.match(name or ""):
        fail(f"plugin.json name {name!r} is not kebab-case")
    if gemini.get("name") != name:
        fail("gemini-extension.json name differs from plugin.json name")
    version = plugin.get("version")
    if gemini.get("version") != version:
        fail("gemini-extension.json version differs from plugin.json version")
    entries = market.get("plugins", [])
    if not entries or entries[0].get("name") != name:
        fail("marketplace.json first plugin name differs from plugin.json name")
    if entries and entries[0].get("source") != "./":
        fail("marketplace.json plugin source should be './' (repo root is the plugin)")
    if "name" not in market.get("owner", {}):
        fail("marketplace.json owner.name is required")
    changelog = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8") if (ROOT / "CHANGELOG.md").is_file() else ""
    match = re.search(r"^## \[?v?(\d+\.\d+\.\d+)", changelog, re.M)
    if not match or match.group(1) != version:
        fail(f"CHANGELOG.md top version {match.group(1) if match else None} != plugin.json version {version}")
    if not (ROOT / "docs/releases" / f"v{version}.md").is_file():
        fail(f"docs/releases/v{version}.md is missing")


def check_skills():
    found = {p.name for p in SKILLS.iterdir() if p.is_dir()}
    if found != EXPECTED_SKILLS:
        fail(f"skills/ contains {sorted(found)}; expected {sorted(EXPECTED_SKILLS)} "
             "(skills/ is auto-discovered wholesale: every folder ships to users)")
    for skill_dir in sorted(SKILLS.iterdir()):
        if not skill_dir.is_dir():
            continue
        skill_md = skill_dir / "SKILL.md"
        if not skill_md.is_file():
            fail(f"{rel(skill_dir)}: missing SKILL.md")
            continue
        if not (skill_dir / "README.md").is_file():
            fail(f"{rel(skill_dir)}: missing README.md (human-facing doc beside SKILL.md)")
        fm, body = parse_frontmatter(skill_md)
        if fm is None:
            fail(f"{rel(skill_md)}: no frontmatter")
            continue
        name = fm.get("name", "")
        if name != skill_dir.name:
            fail(f"{rel(skill_md)}: name {name!r} != folder {skill_dir.name!r}")
        if not NAME_RE.match(name) or len(name) > 64:
            fail(f"{rel(skill_md)}: invalid name {name!r}")
        if "claude" in name or "anthropic" in name:
            fail(f"{rel(skill_md)}: skill names may not contain 'claude' or 'anthropic'")
        desc = fm.get("description", "")
        if not desc:
            fail(f"{rel(skill_md)}: missing description")
        if len(desc) > 1024:
            fail(f"{rel(skill_md)}: description is {len(desc)} chars (max 1024)")
        if "<" in desc or ">" in desc:
            fail(f"{rel(skill_md)}: description contains angle brackets")
        if len((body or "").splitlines()) > 500:
            fail(f"{rel(skill_md)}: body exceeds 500 lines")
        extra = set(fm) - {"name", "description", "license", "compatibility"}
        if extra:
            fail(f"{rel(skill_md)}: unexpected frontmatter keys {sorted(extra)}")
        # every bundled path mentioned in backticks must exist somewhere in skills/
        for token in re.findall(r"`((?:references|templates|scripts)/[^`\s]+)`", skill_md.read_text(encoding="utf-8")):
            if any(ch in token for ch in "<*") or token.endswith("/"):
                continue
            if not any((s / token).exists() for s in SKILLS.iterdir() if s.is_dir()):
                fail(f"{rel(skill_md)}: references `{token}` which does not exist in any skill")
    main = SKILLS / MAIN_SKILL
    if main.is_dir():
        main_text = (main / "SKILL.md").read_text(encoding="utf-8")
        for ref in sorted((main / "references").glob("*.md")):
            if f"references/{ref.name}" not in main_text:
                fail(f"{rel(ref)} is not linked from the main SKILL.md")


def check_agents_and_commands():
    agents = {p.name for p in (ROOT / "agents").glob("*") if p.is_file()}
    if agents != EXPECTED_AGENTS:
        fail(f"agents/ contains {sorted(agents)}; expected {sorted(EXPECTED_AGENTS)} "
             "(every .md in agents/ becomes a subagent; keep docs elsewhere)")
    for path in (ROOT / "agents").glob("*.md"):
        fm, _ = parse_frontmatter(path)
        if not fm or not fm.get("description") or not fm.get("name"):
            fail(f"{rel(path)}: agent needs name and description")
        elif fm["name"] != path.stem:
            fail(f"{rel(path)}: name {fm['name']!r} != filename")
        if fm:
            for banned in ("hooks", "mcpServers", "permissionMode"):
                if banned in fm:
                    fail(f"{rel(path)}: plugin agents may not set {banned}")
    for path in (ROOT / "commands").glob("*.md"):
        fm, _ = parse_frontmatter(path)
        if not fm or not fm.get("description"):
            fail(f"{rel(path)}: command needs a description")
        if path.stem in EXPECTED_SKILLS:
            fail(f"{rel(path)}: a command with a skill's name registers that name twice")


def check_evals():
    evals = ROOT / "evals"
    cases = [p for p in evals.iterdir() if p.is_dir()]
    if len(cases) < 5:
        fail("evals/ should contain at least 5 case folders")
    for case in sorted(cases):
        if not re.match(r"^[a-z][a-z0-9-]*$", case.name):
            fail(f"{rel(case)}: bad case name")
        prompt = case / "prompt.md"
        yaml = case / "case.yaml"
        graders = sorted((case / "graders").glob("*.md")) if (case / "graders").is_dir() else []
        if not prompt.is_file() or not yaml.is_file() or not graders:
            fail(f"{rel(case)}: needs prompt.md, case.yaml and at least one grader")
            continue
        fm, body = parse_frontmatter(prompt)
        if fm is None:
            fail(f"{rel(prompt)}: needs a settings block")
        else:
            unknown = set(fm) - EVAL_PROMPT_KEYS
            if unknown:
                fail(f"{rel(prompt)}: unknown settings keys {sorted(unknown)} (case would fail to load)")
        if not (body or "").strip():
            fail(f"{rel(prompt)}: empty prompt body")
        text = yaml.read_text(encoding="utf-8")
        if 'schema_version: "1.1"' not in text:
            fail(f'{rel(yaml)}: needs schema_version: "1.1" (quoted)')
        if f"name: {case.name}" not in text:
            fail(f"{rel(yaml)}: name must equal folder name")
        if "expected_outcome: |" not in text:
            fail(f"{rel(yaml)}: needs expected_outcome: |")
        for grader in graders:
            if not re.match(r"^\d\d-[a-z0-9-]+\.md$", grader.name):
                fail(f"{rel(grader)}: grader files are numbered NN-few-words.md")
            gfm, gbody = parse_frontmatter(grader)
            if not gfm or gfm.get("type") != "llm" or gfm.get("focus") != "trace" or gfm.get("weight") != "1":
                fail(f"{rel(grader)}: needs type: llm, focus: trace, weight: 1")
            if not (gbody or "").strip():
                fail(f"{rel(grader)}: empty grader")
    queries = read_json(evals / "trigger-queries.json")
    if isinstance(queries, list):
        yes = sum(1 for q in queries if q.get("should_trigger") is True)
        no = sum(1 for q in queries if q.get("should_trigger") is False)
        if yes < 8 or no < 8:
            fail(f"evals/trigger-queries.json needs >=8 positive and >=8 negative (has {yes}/{no})")
    # no results may be committed: honesty guard
    if (evals / "results").exists() or (evals / "snapshots").exists():
        fail("evals/ contains results or snapshots; this repo publishes no measured results")


# ----------------------------------------------------------------- scripts
def check_scripts():
    for path in ROOT.rglob("*.sh"):
        if ".git" in path.parts:
            continue
        result = subprocess.run(["bash", "-n", str(path)], capture_output=True, text=True)
        if result.returncode != 0:
            fail(f"{rel(path)}: bash -n failed: {result.stderr.strip()}")
    for path in ROOT.rglob("*.py"):
        if ".git" in path.parts or "__pycache__" in path.parts:
            continue
        try:
            compile(path.read_text(encoding="utf-8"), str(path), "exec")
        except SyntaxError as exc:
            fail(f"{rel(path)}: {exc}")
    for path in list((SKILLS / "verification-plan/scripts/hooks").glob("*.sh")) + [ROOT / "install.sh"]:
        if path.name != "_lib.sh" and not path.stat().st_mode & 0o111:
            fail(f"{rel(path)}: not executable")


def check_example_sync():
    src_dir = SKILLS / "verification-plan/scripts/hooks"
    dst_dir = ROOT / "examples/hardened-project/.claude/hooks"
    for src in src_dir.glob("*.sh"):
        dst = dst_dir / src.name
        if not dst.is_file() or not filecmp.cmp(src, dst, shallow=False):
            fail(f"{rel(dst)} differs from {rel(src)} (run: make sync-example)")


def check_checksums():
    manifest = ROOT / "CHECKSUMS.sha256"
    if not manifest.is_file():
        return
    for line in manifest.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        digest, _, name = line.partition("  ")
        target = ROOT / name
        if not target.is_file():
            fail(f"CHECKSUMS.sha256 lists missing file {name}")
        elif hashlib.sha256(target.read_bytes()).hexdigest() != digest:
            fail(f"checksum mismatch for {name} (run: make checksums)")


def check_package_reproducible():
    archive = ROOT / "dist" / f"{MAIN_SKILL}.skill"
    if not archive.is_file():
        fail(f"dist/{MAIN_SKILL}.skill missing (run: make package)")
        return
    import importlib.util
    spec = importlib.util.spec_from_file_location("package_skill", ROOT / "scripts/package_skill.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    if module.build_bytes(SKILLS / MAIN_SKILL) != archive.read_bytes():
        fail("dist skill archive is stale; rebuild with: make package")


# ---------------------------------------------------------------- content
def iter_markdown():
    for path in ROOT.rglob("*.md"):
        if ".git" in path.parts:
            continue
        yield path


def check_links():
    link_re = re.compile(r"(?<!!)\[[^\]]*\]\(([^)\s]+)\)")
    for path in iter_markdown():
        in_fence = False
        for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            if line.lstrip().startswith("```"):
                in_fence = not in_fence
                continue
            if in_fence:
                continue
            for target in link_re.findall(line):
                if re.match(r"^(https?:|mailto:|#)", target):
                    continue
                file_part = target.split("#", 1)[0]
                if file_part and not (path.parent / file_part).exists():
                    fail(f"{rel(path)}:{number}: broken link {target}")


def check_numbers_have_provenance():
    provenance = (ROOT / "docs/PROVENANCE.md").read_text(encoding="utf-8")
    number_re = re.compile(r"\d{1,3}(?:,\d{3})+|\d+%")
    for path in SKILLS.rglob("*.md"):
        for match in set(number_re.findall(path.read_text(encoding="utf-8"))):
            if match not in provenance:
                fail(f"{rel(path)}: figure {match!r} is not recorded in docs/PROVENANCE.md")


def check_policy_text():
    for name in ("README.md", "SECURITY.md", "TRADEMARKS.md"):
        text = (ROOT / name).read_text(encoding="utf-8")
        if "unofficial" not in text.lower() and name == "README.md":
            fail("README.md must say the project is unofficial")
    if "Anthropic" in (ROOT / "LICENSE").read_text(encoding="utf-8"):
        fail("LICENSE should not name Anthropic")


def main() -> int:
    for check in (
        check_required_files, check_json_files, check_manifests, check_skills,
        check_agents_and_commands, check_evals, check_scripts, check_example_sync,
        check_checksums, check_package_reproducible, check_links,
        check_numbers_have_provenance, check_policy_text,
    ):
        try:
            check()
        except Exception as exc:  # noqa: BLE001 - report, never hide
            fail(f"{check.__name__} crashed: {exc!r}")
    if failures:
        print(f"{len(failures)} problem(s):")
        for message in failures:
            print(f" - {message}")
        return 1
    print("verify_repo: all checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
