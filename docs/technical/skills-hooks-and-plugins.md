# Skills, agents, commands and hooks

How Claude Code finds each piece in this repo, and the traps. Facts below come from the Claude Code plugins reference fetched on 2026-11-12 (see [Provenance](../PROVENANCE.md)). Check it for changes.

## Plugin manifest

- `.claude-plugin/plugin.json` is the manifest. Only `name` is required. Keep only the manifest inside `.claude-plugin/`; every component folder sits at the plugin root.
- This repo sets no `skills`, `agents` or `commands` keys. Default scanning finds them. A `skills` key would add to the default scan; an `agents` or `commands` key would replace the default folder, which is an easy way to silently ship nothing.
- `.claude-plugin/marketplace.json` lists the plugin with `"source": "./"`. `owner.name` is required.

## Skills

- `skills/<name>/SKILL.md` with `name` equal to the folder and a `description`. The description is the trigger: it decides when Claude loads the skill, so it states both what the skill does and when to use it.
- Every folder under `skills/` ships to every plugin user. Do not park work-in-progress there.
- Skill names may not contain "claude" or "anthropic" if you want claude.ai to save them as skills. Descriptions stay under 1024 characters with no angle brackets.
- `README.md` beside each `SKILL.md` is for people browsing the repo. `SKILL.md` is for the model. They differ on purpose.
- Keep `SKILL.md` short and route to `references/` for depth, so the model loads detail only when needed.

## Agents

- Every `.md` in `agents/` becomes a subagent, named from its frontmatter or filename. Documentation does not belong there.
- Supported frontmatter used here: `name`, `description`, `model`, `maxTurns`, `disallowedTools`. Plugin agents cannot set `hooks`, `mcpServers` or `permissionMode`.

## Commands

- `commands/*.md` load as flat skills next to `skills/*/SKILL.md`. A command with the same name as a skill registers that name twice, so `verify_repo.py` rejects it. The one command here, `stuck-points`, has no skill twin.

## Hooks

- This plugin ships **no** `hooks/hooks.json`, so installing it registers no hooks. Hook scripts are examples under `skills/verification-plan/scripts/hooks/` that you copy and register yourself.
- Event names used by the examples: `PostToolUse`, `TaskCompleted`, `Stop`. Exit code 2 is the signal to send Claude back to fix; exit 1 is not. Per the third-party guide the repo relied on, `PostToolUse` cannot undo a tool call that already ran, and Claude Code caps repeated `Stop` blocks. The example stop hook keeps its own cap as well, because that behavior should not be a hidden dependency.
- Hook scripts read a JSON event on stdin. The examples use `python3` to read fields so `jq` is not required.

## Distribution paths

| Path | How |
|---|---|
| Claude Code plugin | `/plugin marketplace add saptrshighosh/<repo>` then `/plugin install autonomous-coding-sessions@autonomous-coding-sessions` |
| Personal skills folder | `./install.sh` copies the four skill folders to `~/.claude/skills` |
| Single skill archive | `dist/autonomous-coding-sessions.skill` (the core skill only) |
