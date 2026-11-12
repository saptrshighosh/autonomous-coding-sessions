# CLAUDE.md trim checklist

Go through the file one line at a time. For each line, answer in order and stop at the first match.

1. **Could Claude find this by reading the repo or running it?** (stack, directory layout, where to look, how tests are named) -> delete.
2. **Is it only emphasis?** ("IMPORTANT", "NEVER", "ALWAYS", exclamation marks, repeated reminders) -> rewrite as a plain statement of the fact, or delete if there is no fact left.
3. **Is it a hard limit that must never be violated?** -> move it to a deny rule (see `deny-rules.settings.json`). CLAUDE.md is guidance, not enforcement.
4. **Is it a fact that is invisible in the code and still true?** (for example: a service that still depends on a legacy source that no code references) -> keep, and state why it matters.
5. **Is it something you wrote for an older model?** -> try deleting it and compare behavior. Re-audit whenever the model changes.

After trimming, the file should contain only the things Claude cannot see in the code. A short file is the goal, not a side effect.
