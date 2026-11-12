# Provenance

Where every claim in this repo comes from, so you can judge how far to trust it. The rule for this repo: a figure or factual claim appears in a skill only if it is recorded here. `tests/verify_repo.py` enforces that for numbers.

## Source

A public conference talk, "Rethinking Claude Code Best Practices", by a member of the Claude Code team at Anthropic, recorded in late 2026. This repo works from a transcript of it. The transcript has no timestamps, so claims are located by topic, not by time. The speaker is not named in this repo; the talk is credited by title.

Nothing here was independently re-run or re-measured. Where the talk cites another Anthropic publication, we have not read that publication.

## Figures, exactly as the talk stated them

| Figure | As stated | Used in |
|---|---|---|
| 14% | "only about 14% of people caught a clearly dangerous command" in a study Anthropic published in August comparing auto mode with people in the loop | `references/04-safety-layers.md`, main `SKILL.md`, `reversibility-check`, `autonomy-audit` |
| 89% | auto mode "blocked 89% of them" (the same clearly dangerous commands) | same files |
| 1 in 10 | "about 1 in 10 of those commands still went through" auto mode | same files |
| 2,500 | Anthropic went "from about 2,500 changes a day in May" per an Anthropic blog post | `references/01-loop-shift.md` |
| 30,000 | "to more than 30,000 a day in September" | `references/01-loop-shift.md` |

Notes: the talk does not give a sample size, confidence interval or definition of "clearly dangerous" for the study. "About 1 in 10" is the speaker's rounding of the complement of 89%.

## Behavioral claims from the talk

| Claim | Where used |
|---|---|
| Auto mode runs a separate classifier on nearly everything that is not reading or editing project files; allows commands known to be safe, blocks the unsure | `03-auto-mode.md` |
| Auto mode became the default permission mode in August | `03-auto-mode.md` |
| By default auto mode trusts only the current folder and repo; pushing to a separate deploy repo gets blocked | `03-auto-mode.md` |
| Auto mode can be configured in plain English in settings: trusted repos, buckets, domains; always allow; never do | `03-auto-mode.md`, `templates/auto-mode-policy.md` |
| A deny-rule match is checked before the classifier, which never sees the call | `04-safety-layers.md` |
| Rule of thumb: "if Claude gets this wrong once, can I take it back?" | `04-safety-layers.md`, `reversibility-check` |
| A `.env` deny rule means commands like `cat` cannot open it | `04-safety-layers.md` (flagged in `HONEST-LIMITS.md`) |
| Permissions decide whether a call runs, not what it can reach once running; `npm test` can execute compromised dependency code | `04-safety-layers.md` |
| Sandbox: OS-enforced file, folder and host limits, applies to child processes; defaults can still read most of the machine; covers only shell commands, not Claude's own file tools, MCP servers or hooks | `04-safety-layers.md` |
| Cloud session: own machine, fresh repo copy, runs with laptop closed, secrets not in git absent, network secrets, network defaults to package registries and GitHub, commits/pushes/messages leave through connectors | `04-safety-layers.md` |
| Verification checkpoints return pass/fail; prompt-based setup is not guaranteed, hooks are | `05-verification-and-hooks.md`, `verification-plan` |
| Hook examples: lint after edit, tests for changed code when a task completes, full suite at session finish | same |
| Hook scripts must exit 2, not 1, to send Claude back to fix | same |
| CI runs the same checks on every session's PR; CI auto-fix; merge-when-ready (not default, risk-dependent) | `06-scaling-ci-review.md` |
| Fresh-context AI review with a separate group of agents double-checking each bug | `06-scaling-ci-review.md` |
| Review depth by risk: docs/copy none after green checks, ordinary one reviewer, risky two | `06-scaling-ci-review.md`, `templates/risk-tier-matrix.md` |
| Orchestrator session starts and verifies threads, does not write code; orchestrator model good at deciding/judging (example: Fable), thread model good at doing (example: Opus 5.5); set separately; Claude Code projects (beta) handle context automatically | `07-orchestration.md` |
| Recommended first experiment: one much bigger task, CI that catches what you care about, configure network access / secrets / setup script, start in the cloud, find where you are still in the loop | `08-adoption-checklist.md` |
| CLAUDE.md should contain only what Claude cannot see in the code; emphasis can hurt modern models | `02-claude-md-hygiene.md` |
| A command audits CLAUDE.md and skills against a model | `02-claude-md-hygiene.md`. The transcript garbled its name, so none is given |

## Added by this repo (not from the talk)

These are our design choices or interpretations. Treat them as proposals.

- The `ACS_*` environment variable names, the "do nothing if unset" behavior, and the retry cap (`ACS_MAX_BLOCKS`, default 5) in the example hooks.
- The audit script's checks, the 150-line `CLAUDE.md` threshold, and its emphasis-word list.
- The seven-rule summary, the maturity ladder in `08-adoption-checklist.md` (laid out from the talk's order of topics), and the "stuck points" log format.
- The `fresh-context-reviewer` agent: a one-agent approximation of the talk's fresh context plus separate verifying agents.
- Example CI, deny rule paths (`Read(./.env)` etc.), and the hardened example project.

## Facts from outside the talk

| Fact | Source | Fetched |
|---|---|---|
| `plugin.json` fields (`name` required), directory auto-discovery, agent and command frontmatter, `hooks/hooks.json` shape | Claude Code plugins reference, <https://code.claude.com/docs/en/plugins-reference> | 2026-11-12 |
| `marketplace.json` top-level fields and plugin entry fields | Claude Code marketplace reference, <https://code.claude.com/docs/en/plugins/marketplace-reference.md> | 2026-11-12 |
| Hook event names including `TaskCompleted`; exit code 2 on `PostToolUse` and `Stop`; stdin fields | A third-party hooks guide, <https://alexcloudstar.com/blog/claude-code-hooks-guide-2026/>, not the official reference (the official page could not be fetched in the session). Confirm at <https://docs.anthropic.com/en/docs/claude-code/hooks> | 2026-11-12 |
| Repository layout conventions (skill folders with a human README beside `SKILL.md`, plugin auto-discovery pitfalls, evals layout, policy files) | The public `caveman` repository by Julius Brussee, read from a local copy. Layout was used as a structural model; no text or code was copied | 2026-11-12 |
| Eval case folder format | The skill-creator reference in the authoring environment | 2026-11-12 |

## Updating

When a claim changes, edit the skill and this file together. When you add a figure, add its row here first, or `tests/verify_repo.py` will fail.
