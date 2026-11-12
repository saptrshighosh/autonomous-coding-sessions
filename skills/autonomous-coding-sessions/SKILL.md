---
name: autonomous-coding-sessions
description: Playbook for running Claude Code with little or no human supervision (long-running, parallel and orchestrated sessions) while keeping it safe and its output correct. Use this whenever the user wants to set up or reason about a Claude Code workflow for autonomy; configure auto mode; write deny rules; choose between a sandbox and a cloud session; fix hook exit codes; slim down a CLAUDE.md; set up CI auto-fix, merge-when-ready or risk-based review; run many sessions at once; or build an orchestrator with worker threads. Also use when they ask how to stay safe and keep quality high once they stop approving every command, even if they never say "autonomy".
---

# Autonomous Coding Sessions

How to work with current-generation models in Claude Code once you step out of the approval loop. This is a compilation of one public conference talk by the Claude Code team at Anthropic. `docs/PROVENANCE.md` in the repo says what came from where, and `docs/HONEST-LIMITS.md` says what is unverified. This skill is unofficial.

## The one idea

A human used to do five jobs: steer, approve, restrict, check, start. When you stop doing a job, something else must take it over, or there is a gap.

| Job you used to do | Who takes it over | Read |
|---|---|---|
| Steering mid-session | The model (use the newest one, trim CLAUDE.md) | `references/01-loop-shift.md`, `references/02-claude-md-hygiene.md` |
| Approving every command | Auto mode, plus deny rules for hard limits | `references/03-auto-mode.md` |
| Restricting what is possible | The environment: deny rules, sandbox, cloud session | `references/04-safety-layers.md` |
| Checking the output | Pass/fail checkpoints, hooks, CI, an independent reviewer | `references/05-verification-and-hooks.md`, `references/06-scaling-ci-review.md` |
| Starting sessions | An orchestrator session | `references/07-orchestration.md` |

For any step the user wants to automate, ask: "If I am no longer here, what takes over?" If the honest answer is "nothing", close that gap first. To roll everything out in order, use `references/08-adoption-checklist.md`.

## Rules that carry most of the value

1. **Hard limits belong in the harness or environment, not in the model's judgment.** In the talk's study, people in the loop caught about 14% of clearly dangerous commands and auto mode blocked about 89%. That leaves roughly 1 in 10 through, so anything that must never happen needs a deny rule (checked before the classifier ever sees the call) or an environment that cannot do it.
2. **Decide what becomes a rule with one question:** if Claude gets this wrong once, can I take it back? Wrong code can be reverted, so trust the model. Discarding uncommitted work or reading a secret into the transcript cannot be undone, so make it a rule.
3. **Permissions decide whether a call runs, not what it can reach once running.** `npm test` looks harmless but executes dependency code. Limit its reach with a sandbox, or better a cloud session that never held your secrets.
4. **You are no longer watching, so build pass/fail checkpoints.** Prompting for them is easy but not guaranteed. Hooks are guaranteed.
5. **A hook that must send Claude back to fix something exits with code 2, not 1.** Exit 1 lets the task be marked complete anyway.
6. **Keep CLAUDE.md to what Claude cannot see in the code.** Shouted instructions ("IMPORTANT", "NEVER") cost tool calls and can push modern models off track.
7. **CI is the backstop for every session.** Review depth should scale with risk, and the reviewer should be a fresh context, not the session that wrote the change.

## Sibling skills in this plugin

Use these for the hands-on workflows. Each is self-contained.

| Skill | Use it to |
|---|---|
| `autonomy-audit` | Audit a project's Claude Code setup with a read-only script and explain the findings |
| `reversibility-check` | Decide whether an action should be left to the model, a deny rule, a sandbox, or a cloud session |
| `verification-plan` | Turn a task into pass/fail checkpoints, and wire the must-run ones as hooks |

## How to help the user

- **"Is this safe to automate?"** Apply rule 2 to each action, then pick the layer from the table in `references/04-safety-layers.md`.
- **Writing config:** start from `templates/` here. Treat every setting name and the exact syntax as something to verify against the current Claude Code docs. The source talk describes behavior, not syntax, and these details change.
- **Keep it proportional.** A one-off script does not need an orchestrator. A production change does need deny rules, checks, and a human reviewer.
- **Do not invent numbers.** The only figures in this skill are the ones in `docs/PROVENANCE.md`, reported as the talk stated them.

## Bundled files

- `references/`: eight topic files, loaded as needed.
- `templates/`: starting points for deny rules, an auto mode policy, a CLAUDE.md audit checklist, and a risk-tier review matrix (see `templates/README.md`).
