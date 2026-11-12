# 05. Verification and hooks

## Why this matters once you are gone

When you reviewed every change you knew the work was good. After hours of background work you do not have that, and you will not read every file at the end.

The model is good at understanding what you want, but it still makes many small decisions. The talk's example: ask it to move auth to a new API. With the same prompt, one run might migrate but leave the old API in place, another might migrate only new logins, another might log everyone out. All look reasonable.

## Checkpoints

Add verification points that come back as **pass or fail**: tests, a build, a screenshot, anything checkable.

- Claude keeps verifying its own results against them.
- You review the checkpoints, which is far shorter than reviewing the whole change.
- A run that logs everyone out fails the check and must find another way.

## Two ways to set them up

### 1. In the prompt (easy, not guaranteed)

- Say what "done" looks like.
- Ask Claude to split the work into tasks, each with its own tests.
- Ask it to show the actual output, because you were not there to see it.

The `verification-plan` skill's `templates/verification-plan.md` is a fill-in version of this.

### 2. With hooks (guaranteed)

Hooks are scripts Claude Code runs at a specific point. You decide when they run, what they run, and what they check. The talk's examples:

| When | What runs |
|---|---|
| After each file edit | The linter |
| When Claude wants to mark a task complete | The tests for what it changed (touched auth code means auth tests must pass) |
| When Claude wants to finish the whole session | The entire test suite |

If a check fails, Claude goes back until it passes.

## The exit code gotcha

Most tools exit with code **1** when a test fails. In Claude Code a hook that exits 1 lets the task be marked completed anyway. A hook that exits **2** is what actually sends Claude back to fix the problem. Make sure your scripts translate a failure into exit 2.

## Example scripts in this repo

All under the `verification-plan` skill's `scripts/hooks/`, opt-in, never auto-registered:

| Script | Intended event | Reads |
|---|---|---|
| `lint-on-edit.sh` | after a file edit | `ACS_LINT_CMD` (run with the edited file path as its argument) |
| `tests-on-task-complete.sh` | task marked complete | `ACS_TASK_TEST_CMD` |
| `full-suite-on-stop.sh` | session wants to finish | `ACS_TEST_CMD`, `ACS_MAX_BLOCKS` (default 5) |

Design choices that are ours, not the talk's: each script does nothing if its command variable is unset, so installing it cannot break a project; the stop script counts consecutive blocks per session and gives up after `ACS_MAX_BLOCKS` so a permanently failing suite cannot trap a session forever. That skill's `templates/hooks.settings.json` shows how to register them.

## Facts to confirm before relying on them

The talk describes hook behavior in outline. The event names and exit-code semantics below come from a third-party summary of the docs, not from the talk, so confirm them in the official hooks reference:

- `PostToolUse`: the tool already ran, so exit 2 surfaces the message to Claude but cannot undo the call.
- `TaskCompleted`: exit 2 blocks the task from being marked complete.
- `Stop`: exit 2 stops Claude from finishing and feeds the message back.
- Claude Code itself caps repeated Stop blocks, but do not depend on that: keep your own cap.

## Beyond hooks

Hooks guard one session. For the same checks across every session, run them in CI (`06-scaling-ci-review.md`), which does not depend on how the session was configured.
