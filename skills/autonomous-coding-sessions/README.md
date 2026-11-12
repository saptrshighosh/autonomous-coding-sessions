# autonomous-coding-sessions

The core playbook for running Claude Code with little or no human supervision.

## What it does

When you stop approving every command, something else has to take over. This skill gives Claude the map: which job (steer, approve, restrict, check, start) is now done by the model, the harness, or the environment, and what to configure so nothing is left uncovered.

It is a compilation of one public conference talk by the Claude Code team at Anthropic. It is unofficial, and claims are reported as the talk stated them. See [`docs/PROVENANCE.md`](../../docs/PROVENANCE.md) and [`docs/HONEST-LIMITS.md`](../../docs/HONEST-LIMITS.md).

## What is inside

| Path | Purpose |
|---|---|
| `SKILL.md` | The prompt body Claude loads: the one idea, seven rules, routing to references |
| `references/` | Eight topic files, read only when needed |
| `templates/` | Deny rules, auto mode policy, CLAUDE.md checklist, risk-tier matrix |

## Ask it things like

- "Audit how safe my Claude Code setup is for running overnight."
- "Should reading `.env` be a deny rule or can I trust the model?"
- "Why does my test hook not stop Claude from finishing?"
- "Help me go from one session to an orchestrator with workers."

## Related skills in this repo

`autonomy-audit`, `reversibility-check`, and `verification-plan` handle the hands-on workflows.

`SKILL.md` is the LLM-facing prompt; this file is for people browsing the repo. They are kept separate on purpose.
