# Install

Pick one path. All of them only add skills (and, for the plugin, agents and one command). **Nothing here registers a hook or edits your settings.**

## 1. Claude Code plugin

After the repo is on GitHub (yours or a fork), inside Claude Code:

```
/plugin marketplace add saptrshighosh/autonomous-coding-sessions
/plugin install autonomous-coding-sessions@autonomous-coding-sessions
```

Check that it loaded with `/plugin`. The marketplace entry uses `"source": "./"`, so the repo root is the plugin.

## 2. Copy the skills into your personal folder

```bash
git clone https://github.com/saptrshighosh/autonomous-coding-sessions
cd autonomous-coding-sessions
./install.sh --list        # see what would be copied
./install.sh               # copy to ~/.claude/skills (or $CLAUDE_CONFIG_DIR/skills)
./install.sh --dest DIR    # copy somewhere else
./install.sh --uninstall   # remove only the four skills this script installs
```

Read `install.sh` first: it is about forty lines. It copies four folders and nothing else.

## 3. Upload the core skill in claude.ai

Use `dist/autonomous-coding-sessions.skill` (the core skill only). The other three skills are not in that archive. This path was not tested end to end.

## 4. Project-local

Copy the skill folders you want into `<your-project>/.claude/skills/` to share them with your team through git.

## Using the example hooks (opt-in, separate)

The hook scripts are not part of any install above. To use them:

1. Copy `skills/verification-plan/scripts/hooks/` into your project, e.g. to `.claude/hooks/`.
2. Merge `skills/verification-plan/templates/hooks.settings.json` into `.claude/settings.json`.
3. Set `ACS_LINT_CMD`, `ACS_TASK_TEST_CMD` and `ACS_TEST_CMD` to your commands.

`examples/hardened-project/` shows a complete small version.

## Verify what you downloaded

```bash
python3 scripts/gen_checksums.py --check   # files match CHECKSUMS.sha256
make check                                 # full test and verification run
```

Checksums catch accidental or partial changes. They do not prove who wrote the files, so pin to a release tag and read the diff.

## Requirements

bash and Python 3 (standard library only). No Node, no network. Windows is unsupported (no PowerShell installer).

## Troubleshooting

- **Skill does not trigger:** check that it appears in Claude Code's skill list, then try a prompt close to the examples in `evals/`. Trigger tuning has not been done.
- **`install.sh: permission denied`:** run `bash install.sh` or `chmod +x install.sh`.
- **A hook script does nothing:** that is by design until you set its `ACS_*` variable.
- **Anything else:** ask Claude to read `CLAUDE.md` and this file, or open an issue.
