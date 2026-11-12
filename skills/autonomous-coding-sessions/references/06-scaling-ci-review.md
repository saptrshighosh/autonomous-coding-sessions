# 06. Scaling up: parallel sessions, CI, and review

## From one trusted session to several

Once one session is safe to leave alone, start more.

- Each cloud session has its own machine, so they do not all work in one folder, and you rarely need to think about worktrees yourself.
- You still start every session and review every result at this stage. The talk calls this a good place to be: you stay fully in control of what starts and when a task counts as done.

## CI is the backstop

Every session eventually opens a pull request. CI runs the same checks on every one of them, regardless of how the session was set up or what Claude decided along the way. So the most important thing to have in place is a CI that **actually catches the things you care about**.

- **CI auto-fix:** Claude sees when a check fails and goes back to fix it, so your review time is not spent on things a check already caught.
- **Merge when ready:** GitHub merges the PR once all checks pass, so you are not in the loop to review. This is not the default, and whether it is appropriate depends on how risky the change is.

## Independent review

In the talk's team, every PR is reviewed by Claude first, and not by the session that wrote it.

- It starts with a **fresh context**.
- A **separate group of agents** double-checks every bug it finds.
- A human's involvement then depends on risk.

The repo's `agents/fresh-context-reviewer.md` is a starting point for the same idea, but it is our interpretation of the pattern, not the talk's implementation.

## Review depth scales with risk

| Change | Review (as described in the talk) |
|---|---|
| Small: docs, copy | No person needed once automated checks are green |
| Ordinary product change | One reviewer |
| Risky change | Two reviewers |

`templates/risk-tier-matrix.md` is a fill-in version. The tiers are examples. Decide what counts as risky for your system, and write it down before you enable merge-when-ready for anything.

## Common failure modes to check for

- CI passes but does not test the behavior you care about. Parallelism then just produces confident, unverified changes faster.
- Merge-when-ready enabled for changes that the matrix says need a person.
- The author session is also the reviewer.
