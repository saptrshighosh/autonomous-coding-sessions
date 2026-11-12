# hardened-project (example)

A tiny, fake project showing what the `autonomy-audit` skill considers a reasonable baseline for unattended runs:

- a short `CLAUDE.md` with only a fact that is invisible in the code
- deny rules for `.env` files and SSH keys, committed in `.claude/settings.json`
- the three example hooks registered (`PostToolUse`, `TaskCompleted`, `Stop`)
- the hook scripts in `.claude/hooks/` (byte-identical copies of the ones in `skills/verification-plan/scripts/hooks/`; `make sync-example` refreshes them)
- a CI workflow and a `.gitignore` that covers `.env`

The hooks do nothing until you set `ACS_LINT_CMD`, `ACS_TASK_TEST_CMD` and `ACS_TEST_CMD`. This is a demonstration, not a drop-in config: replace the placeholder CI step and decide your own deny rules. The audit script exits clean on it, and `tests/test_audit_setup.py` checks that.
