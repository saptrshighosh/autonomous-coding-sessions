---
name: autonomy-audit
description: Audit a project's Claude Code setup for unattended or parallel use and explain each finding. Use when the user asks to audit, review, check or harden their Claude Code setup, CLAUDE.md, permissions, deny rules, hooks or CI before letting sessions run on their own, or asks whether their setup is safe to leave running. Runs a read-only script and reports only what it found.
---

# Autonomy audit

Check what a project has on disk against what unattended sessions need, and explain the gaps.

## Procedure

1. **Find the project directory.** Use the current directory unless the user names another. Ask if it is unclear.
2. **Run the script** (path is relative to this skill's folder; it is read-only and uses only the Python standard library):

   ```bash
   python3 scripts/audit_setup.py <project-dir> --json
   ```

3. **Report by severity**, highest first. For each finding give: what was found, why it matters, and the concrete fix. Keep each to a few lines.
4. **Separate what was measured from what is judgment.** The script reports facts about files on disk (a rule is present or absent, a hook script exits 1 but never 2). Whether that matters for this team is your judgment, so say which is which.
5. **Do not edit the project** unless the user asks. Offer to apply specific fixes afterward.

## What the checks mean

| Finding | Why it matters |
|---|---|
| `CLAUDE_MD_EMPHASIS`, `CLAUDE_MD_LONG` | Shouted emphasis and restated facts cost tool calls and can push modern models off track. Keep only what is invisible in the code. |
| `BYPASS_PERMISSIONS` | Skips the permission checks entirely, including the classifier. |
| `NO_PROJECT_SETTINGS`, `NO_DENY_RULES`, `NO_ENV_DENY`, `NO_SSH_DENY` | Deny rules are the only way to guarantee something never happens: they are checked before the auto mode classifier. Auto mode alone let about 1 in 10 clearly dangerous commands through in the talk's study. |
| `HOOK_EXIT_1` | A hook that exits 1 lets the task complete anyway; exit 2 sends Claude back to fix. |
| `NO_VERIFICATION_HOOK` | Nothing guarantees checks run before Claude finishes. Prompts for checks are not guaranteed; hooks are. |
| `NO_CI` | CI is the backstop that checks every session's PR the same way. |
| `ENV_NOT_IGNORED` | A secret file that reaches git also reaches a cloud session's repo copy. |
| `NO_SANDBOX_KEY` (info) | A sandbox may be configured outside this project (user settings or cloud), so this is only a prompt to check. |

If the main `autonomous-coding-sessions` skill is installed, point to its `references/04-safety-layers.md` and `references/05-verification-and-hooks.md` for depth.

## Limits to state in every report

The script cannot see user-level settings, cloud environment configuration, branch protection rules, or whether CI actually tests what matters. A clean audit means "nothing found on disk", not "safe". Setting names follow the documented Claude Code format; confirm against the current docs.

## Output shape

```
Audit of <dir>: <n> findings (<h> high, <m> medium, <l> low)

HIGH   <id>: <what>
       Why: <one line>   Fix: <one line>
...
Not checked: user-level settings, cloud config, branch protection, CI quality.
```
