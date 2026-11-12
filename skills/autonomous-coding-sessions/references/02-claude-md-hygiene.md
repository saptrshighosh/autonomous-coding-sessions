# 02. Keep CLAUDE.md to what Claude cannot see

## The rule

A CLAUDE.md should contain only what Claude cannot learn from the code. With today's models, instructions that restate what is visible, or that shout, do not help and can make things worse: the model goes off track, makes more tool calls, and produces worse results.

## Keep

- Facts invisible in the repository. The talk's example: a service that still depends on some legacy source that no code references directly.
- Anything else a new engineer could not discover by reading the code and running it.

## Remove

- What stack the project is on.
- Where to look for things.
- Emphasis: "IMPORTANT", "NEVER do this!", exclamation marks, repeated reminders. These were workarounds for older models that stopped early and needed constant correction.

## Re-audit when the model changes

Instructions written for an older model may be dead weight for a newer one. The talk describes a Claude Code command that checks your CLAUDE.md and your skills against a chosen model and reports what that model no longer needs. The talk's transcript garbled the command's name, so this repo does not give one. Look it up in the current Claude Code docs.

## A manual pass (if the command is unavailable)

Use `templates/claude-md-checklist.md`. For each line ask:

1. Could Claude find this by reading the repo? Delete it.
2. Is it emphasis with no new information? Rewrite it plainly or delete it.
3. Is it a hard limit that must never be violated? It does not belong in CLAUDE.md at all. Make it a deny rule (`04-safety-layers.md`), because CLAUDE.md is guidance, not enforcement.
4. Is it a fact that is invisible in the code and still true? Keep it, and say why it matters.

The `autonomy-audit` skill's `scripts/audit_setup.py` flags emphasis markers and very long files. Those are heuristics, not proof that something should go.
