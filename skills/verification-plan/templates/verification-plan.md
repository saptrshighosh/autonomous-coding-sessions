# Verification plan

**Goal (one sentence):**

**What "done" looks like (checkable):**

## Tasks and checks

| # | Task | Check (pass/fail) | Enforced by |
|---|---|---|---|
| 1 | | e.g. `pytest tests/auth` | hook: task complete |
| 2 | | e.g. build succeeds | prompt |
| 3 | | e.g. screenshot matches expected state | prompt |

## Gates

- After each edit: `<linter>` (hook, optional)
- Before the session finishes: `<full test suite>` (hook)
- In CI: `<jobs that must be green>`

## Rules for the run

- Claude must paste the **actual output** of every check, not a summary, because nobody was watching.
- A failing check means the task is not done. Claude finds another way instead of loosening the check.
- Hook scripts exit **2** on failure (exit 1 lets the task complete anyway).

## Review

- What I will review: the checkpoint outputs, not every file.
- Risk tier of this change and who reviews it: `<see risk-tier-matrix.md>`
