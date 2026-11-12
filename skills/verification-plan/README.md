# verification-plan

Turns a task into pass/fail checkpoints and wires the must-run ones as hooks.

## Contents

| Path | Purpose |
|---|---|
| `SKILL.md` | The prompt Claude loads |
| `templates/verification-plan.md` | A fill-in plan: goal, tasks, checks, enforcement |
| `templates/hooks.settings.json` | Example hook registration for a project's `.claude/settings.json` |
| `scripts/hooks/lint-on-edit.sh` | Runs `$ACS_LINT_CMD` on the edited file |
| `scripts/hooks/tests-on-task-complete.sh` | Runs `$ACS_TASK_TEST_CMD` before a task may complete |
| `scripts/hooks/full-suite-on-stop.sh` | Runs `$ACS_TEST_CMD` before a session may finish, with a retry cap |

## Use the hooks by hand

1. Copy `scripts/hooks/` into your project, for example to `.claude/hooks/`.
2. Merge `templates/hooks.settings.json` into `.claude/settings.json`.
3. Set the environment variables for your project's commands.

They are opt-in on purpose. Nothing in this repo registers a hook for you. Hook behavior is covered by `tests/test_hooks.py`. The one-line reason they exit 2: exit 1 lets Claude mark the task complete anyway.

`SKILL.md` is the prompt Claude loads; this file is for people browsing the repo.
