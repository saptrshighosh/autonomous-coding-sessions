# CLAUDE.md: autonomous-coding-sessions

Maintainer instructions for agents working in this repo.

## What this repo is

A knowledge playbook for running Claude Code with little supervision, compiled from one public conference talk, packaged as skills, a plugin, agents, one command, and small tools. It is unofficial. It is not a runtime. See `docs/technical/architecture.md`.

## The honesty rules (these outrank style)

- **No invented numbers.** A figure (a number with `%` or thousands separators) may appear in a skill file only if `docs/PROVENANCE.md` records it. `tests/verify_repo.py` fails otherwise. Add the provenance row first.
- **No invented syntax.** Setting names and hook behavior that the talk did not state must be verified against current docs, or flagged as unverified in the file and in `docs/HONEST-LIMITS.md`.
- **No results without raw data.** Do not commit anything under `evals/results/` or `evals/snapshots/`. Do not claim a skill "improves" anything. The verifier fails if those folders exist.
- **Keep the speaker anonymous.** Credit the talk by title only.
- **Keep it unofficial.** Do not imply Anthropic endorsement.

## What lives where

```
skills/                  SOURCE OF TRUTH, auto-discovered wholesale: every folder ships
  autonomous-coding-sessions/  SKILL.md, README.md, references/, templates/
  autonomy-audit/              SKILL.md, README.md, scripts/audit_setup.py
  reversibility-check/         SKILL.md, README.md
  verification-plan/           SKILL.md, README.md, templates/, scripts/hooks/
agents/                  every .md here becomes a subagent
commands/                names must differ from skill names
examples/hardened-project/    fake project; hook copies are synced
evals/                   cases and graders only
tests/                   unit tests, fixtures, verify_repo.py
scripts/                 package_skill.py, gen_checksums.py
docs/                    trust docs and technical notes
dist/                    reproducible .skill archive
.claude-plugin/          manifests (repo root is the plugin)
```

## Edit only source files

| Edit | Do not edit by hand | Regenerate with |
|---|---|---|
| `skills/verification-plan/scripts/hooks/*.sh` | `examples/hardened-project/.claude/hooks/*` | `make sync-example` |
| any skill folder | `dist/autonomous-coding-sessions.skill` | `make package` |
| any script, manifest, hook | `CHECKSUMS.sha256` | `make checksums` |

`make all` does all three in order, then checks.

## Rules that bite

- **`skills/` is auto-discovered wholesale.** A new folder ships to every user and its description competes for activation. If you add one, update `EXPECTED_SKILLS` in `tests/verify_repo.py`, the README table, and `install.sh`.
- **`agents/*.md` is auto-discovered too.** Do not put docs there. Do not add `agents` or `skills` keys to `plugin.json`: an explicit `agents` key can load nothing, and the default scan is what works.
- **A command named like a skill registers that name twice.** The verifier rejects it.
- **Skill names must not contain "claude" or "anthropic"** if claude.ai is to save them as skills.
- **Each skill has two audiences:** `SKILL.md` is the model's prompt (short, routes to references); `README.md` is for people. Do not merge them.
- **Hook scripts exit 2 on failure, never 1.** `tests/test_hooks.py` enforces it. Hook scripts must do nothing when their `ACS_*` variable is unset.
- **Nothing registers a hook.** Do not add `hooks/hooks.json`: Claude Code auto-loads it from a plugin root and would register hooks for every user.
- **The audit script is read-only.** A test checks it never changes the directory it audits.
- **Bump versions together:** `plugin.json`, `gemini-extension.json`, `CHANGELOG.md`, `docs/releases/vX.Y.Z.md`. The verifier checks they agree.

## Before you finish any change

```bash
make all
```

If a check fails, fix the cause. Do not weaken a check or a grader to make it pass.

## Adding a claim from the talk

1. Add a row to `docs/PROVENANCE.md` saying how the talk stated it and where you use it.
2. Add it to the right file in `skills/autonomous-coding-sessions/references/`.
3. If it is uncertain, add it to `docs/HONEST-LIMITS.md`.
4. If it changes advice, add or adjust an eval case under `evals/`.
