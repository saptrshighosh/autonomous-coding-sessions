# Risk-tier review matrix

Write this down before enabling merge-when-ready for anything. The first three rows are the example tiers from the source talk; adapt the examples and add rows for your own system.

| Tier | Example changes | Automated checks | Fresh-context AI review | Human reviewers | Merge when ready? |
|---|---|---|---|---|---|
| Low | Docs, copy | Must be green | Yes | 0 | Your call. Fill in. |
| Ordinary | Normal product changes | Must be green | Yes | 1 | Your call. Fill in. |
| Risky | `<auth, payments, migrations, infra ... decide>` | Must be green | Yes | 2 | `<usually no>` |

## Questions to settle per tier

- What is the worst case if a wrong change merges? Can it be rolled back quickly?
- Does CI actually exercise the behavior that matters for this tier?
- Who counts as a reviewer, and are they independent of the author session?
- Who decides which tier a change belongs to, and how is that recorded?
