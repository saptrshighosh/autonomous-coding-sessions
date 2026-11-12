---
description: Log where you were still in the loop during an autonomous run, and decide what to hand over next
argument-hint: "[notes on what you had to approve, correct, rerun or start by hand]"
---

Help me find the next thing to hand over to Claude. This is step 5 of the adoption checklist: watch where sessions get stuck and where I am still in the loop.

Here is what I had to do by hand: $ARGUMENTS

If that is empty, ask me for the list in one short question.

For each item:

1. Classify it as one of the five jobs: **steer**, **approve**, **restrict**, **check**, or **start**.
2. Say what could take it over: the **model**, the **harness** (auto mode, deny rules, hooks), or the **environment** (sandbox, cloud session, CI).
3. Say what concrete setup change would do it, and whether it can be done now.

Then give me a short table of the items, sorted so the cheapest handover comes first, and name the single change I should make next. If something should stay human (for example review of a risky change), say so and why.

Use the `autonomous-coding-sessions` skill's references for detail when it is installed. Do not invent numbers or settings syntax; point me to the current Claude Code docs for exact syntax.
