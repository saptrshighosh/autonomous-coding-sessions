# Templates

Starting points, not finished policy. Fill them in for your own project, and verify every setting name and syntax against the current Claude Code docs before relying on it.

| File | What it is | Status |
|---|---|---|
| `deny-rules.settings.json` | Project `.claude/settings.json` fragment denying reads of `.env` files and SSH keys | Syntax follows the documented `permissions.deny` format; whether a `Read(...)` rule also stops `cat` is the talk's claim, so test it (see `docs/HONEST-LIMITS.md`) |
| `auto-mode-policy.md` | Plain-English policy text for auto mode: trusted repos, buckets, domains, always-allow, never | The talk does not say where this text is configured; find the current location in the docs |
| `claude-md-checklist.md` | Line-by-line checklist for trimming CLAUDE.md | Pure process, no syntax |
| `risk-tier-matrix.md` | Fill-in matrix mapping change types to review depth and merge-when-ready eligibility | The three example tiers are from the talk; the rest is for you to decide |

Hook registration and the verification plan template live with the `verification-plan` skill.
