# Architecture

This is a knowledge repo with a little tooling. There is no server, no build step, and no runtime dependency beyond bash and Python 3 (standard library).

## Layout and ownership

```
autonomous-coding-sessions/
├── README.md, INSTALL.md          # front door and install matrix
├── CLAUDE.md, AGENTS.md, GEMINI.md  # instructions for agents working in (or reading) this repo
├── CONTRIBUTING.md, CODE_OF_CONDUCT.md, SECURITY.md, TRADEMARKS.md, NOTICE, LICENSE
├── CHANGELOG.md, CHECKSUMS.sha256 # generated: checksums
├── install.sh                     # copies skill folders; touches nothing else
├── Makefile                       # make all | check | test | package | checksums | sync-example
│
├── .claude-plugin/                # plugin.json + marketplace.json (repo root is the plugin)
├── gemini-extension.json          # reference-only extension manifest
│
├── skills/                        # SOURCE OF TRUTH. Auto-discovered wholesale.
│   ├── autonomous-coding-sessions/  # core playbook: SKILL.md, README.md, references/, templates/
│   ├── autonomy-audit/              # SKILL.md, README.md, scripts/audit_setup.py
│   ├── reversibility-check/         # SKILL.md, README.md
│   └── verification-plan/           # SKILL.md, README.md, templates/, scripts/hooks/
├── agents/                        # subagents (every .md here becomes one)
├── commands/                      # slash commands (names must not equal skill names)
│
├── examples/hardened-project/     # fake project the audit passes; hook scripts are synced copies
├── evals/                         # test cases and graders only. No results are committed.
├── tests/                         # unit tests, fixtures, and verify_repo.py
├── scripts/                       # package_skill.py, gen_checksums.py
├── docs/                          # trust docs, technical notes, release notes
├── dist/                          # the reproducible packaged skill archive
└── .github/                       # CI, issue and PR templates, dependabot
```

## Sources of truth and generated files

| Edit this | Never edit by hand |
|---|---|
| `skills/*/SKILL.md`, `references/`, `templates/`, `scripts/` | `dist/autonomous-coding-sessions.skill` (run `make package`) |
| `skills/verification-plan/scripts/hooks/*.sh` | `examples/hardened-project/.claude/hooks/*` (run `make sync-example`) |
| Any tracked script, manifest, or hook | `CHECKSUMS.sha256` (run `make checksums`) |

`make all` regenerates everything in the right order and then checks it.

## Why the repo root is the plugin

`.claude-plugin/marketplace.json` uses `"source": "./"`, so the plugin root is the repo root and Claude Code discovers `skills/*/SKILL.md`, `agents/*.md` and `commands/*.md` by convention. That means no mirrored `plugins/` copy and no sync workflow, so there is nothing to drift. It also means every skill folder ships to every user, so `verify_repo.py` pins the exact set of skills and agents.

## Why the audit script and hooks live inside skills

Each skill folder is self-contained so it still works when installed alone (for example from `install.sh` or a `.skill` archive). The audit script lives with `autonomy-audit`, the hook scripts with `verification-plan`. The only duplication is the example project's hook copies, which a test keeps byte-identical.

## Data flow

None at runtime. The audit script reads files in the directory you point it at and prints findings. The hook scripts read a JSON event on stdin, run a command you configured, and exit 0 or 2. Nothing is sent anywhere.
