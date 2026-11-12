---
name: verification-plan
description: Turn a coding task into pass/fail checkpoints Claude can verify on its own, and decide which must be enforced by hooks. Use when the user is about to hand Claude a large or long-running task and wants it to verify its own work, asks how to make sure Claude actually runs the tests, asks for hooks that run a linter, task tests or the full suite, or reports that a hook does not stop Claude from finishing (exit code 1 versus 2).
---

# Verification plan

When Claude works for hours unsupervised, you will not read every file at the end. Replace "I saw every change" with checkpoints that return pass or fail.

## Why plain prompting is not enough

The same prompt can give different, reasonable-looking results. Asked to "move auth to the new API", one run may leave the old API in place, another may migrate only new logins, another may log everyone out. A checkpoint turns each of those into a visible failure.

## Procedure

1. **Define "done"** in checkable terms: tests, a build, a screenshot, anything that comes back pass or fail.
2. **Split the work into tasks, each with its own check.** Keep checks small so reviewing them is far faster than reviewing the whole change.
3. **Choose how each check is enforced:**
   - **In the prompt** (easy, not guaranteed): say what done looks like, ask for tasks with their own tests, and ask Claude to show the actual output, since the user was not there to see it.
   - **As a hook** (guaranteed): for checks that must run. Common mapping from the talk:

| When | Check |
|---|---|
| After each file edit | Linter |
| When a task is about to be marked complete | Tests for what changed (touched auth code means auth tests must pass) |
| When the whole session wants to finish | The entire test suite |

4. **Make failing hooks exit with code 2, not 1.** Exit 1 lets the task be marked complete anyway. Exit 2 is what sends Claude back to fix the problem.
5. **Write the plan down** using `templates/verification-plan.md`, then register hooks using `templates/hooks.settings.json` and the scripts in `scripts/hooks/`.

## The example hook scripts

Opt-in, never auto-registered. Each does nothing when its variable is unset, so installing one cannot break a project.

| Script | Intended event | Environment variables |
|---|---|---|
| `scripts/hooks/lint-on-edit.sh` | After a file edit | `ACS_LINT_CMD` (the edited file's path is appended) |
| `scripts/hooks/tests-on-task-complete.sh` | Task marked complete | `ACS_TASK_TEST_CMD` |
| `scripts/hooks/full-suite-on-stop.sh` | Session wants to finish | `ACS_TEST_CMD`, `ACS_MAX_BLOCKS` (default 5) |

`ACS_*` names and the retry cap are this repo's design, not the talk's. The cap stops a permanently failing suite from trapping a session; past it the stop hook allows the session to end, so CI must remain the real backstop.

## Confirm before relying on it

Event names and exit-code behavior (`PostToolUse` cannot block because the tool already ran; `TaskCompleted` and `Stop` can be blocked with exit 2) came from a third-party summary of the docs, not from the talk. Check the official hooks reference.

## Output shape

```
Goal: <one sentence>
Tasks:
1. <task> -> check: <command or artifact> -> enforced by: <prompt | hook event>
...
Final gate: <full suite / CI job>
Show-output rule: Claude must paste the real command output for each check.
```
