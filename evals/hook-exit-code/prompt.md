---
tags: [autonomous-coding-sessions]
max_turns: 12
timeout_seconds: 300
allowed_tools: [Read, Glob, Grep, Skill, Bash]
---

I wrote a Stop hook that runs my test suite, but when tests fail Claude just finishes anyway. The script does `pytest || exit 1`. What's wrong?
