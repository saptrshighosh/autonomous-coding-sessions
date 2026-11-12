# autonomy-audit

Audits a project's Claude Code setup for unattended use, then explains each finding in plain language.

## What it checks

`scripts/audit_setup.py` (Python standard library only, read-only) looks for:

- shouted emphasis words and very long files in `CLAUDE.md`
- `permissions.defaultMode: "bypassPermissions"`
- missing deny rules, especially for `.env` and `.ssh`
- hook scripts that exit 1 on failure and never exit 2
- no `Stop` or `TaskCompleted` hook
- no CI configuration
- `.env` present but not in `.gitignore`

## Run it by hand

```bash
python3 skills/autonomy-audit/scripts/audit_setup.py path/to/project
python3 skills/autonomy-audit/scripts/audit_setup.py path/to/project --json
python3 skills/autonomy-audit/scripts/audit_setup.py path/to/project --fail-on high   # exit 1 on high findings
```

## What it cannot see

User-level settings, cloud environment configuration, branch protection, and whether your CI is any good. Every finding is a heuristic over files on disk: "look at this", not "this is wrong". Tests for it are in `tests/test_audit_setup.py`; they run against a deliberately bad fixture and a hardened example.

`SKILL.md` is the prompt Claude loads; this file is for people browsing the repo.
