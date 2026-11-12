# 03. Auto mode

## What it is

Auto mode is a permission mode that runs a separate classifier on nearly everything that is not just reading or editing files in your project.

- It allows commands it knows are safe, such as running tests or installing dependencies.
- It blocks commands where it is unsure they are safe.
- The talk says it became the default permission mode in August.

## The default trust boundary

By default auto mode trusts only the current folder and repo. Example from the talk: ask Claude to ship something to staging and it needs to push to a separate deploy repo. A human would have approved that push, but auto mode blocks it, so you are back in the loop.

## When you are still approving a lot

If you still approve many commands in auto mode, check settings first. Auto mode can be configured in plain English. That text is what is sent to the classifier, which decides whether to allow or reject a command.

In that text, state:

- which **repos**, **buckets**, and **domains** you trust,
- what it should **always allow**,
- what it should **never** do.

`templates/auto-mode-policy.md` is a fill-in-the-blanks starting point. The talk does not say where that text lives in settings or what the key is called, so find the current location in the Claude Code docs before writing it.

## What auto mode is not

It is not a guarantee. It is much better than people at catching dangerous commands (see the numbers in `04-safety-layers.md`) but about 1 in 10 clearly dangerous commands still got through in the talk's study. Rules that must always hold are enforced elsewhere:

- Deny rules are checked before the classifier. A call that matches one never reaches it.
- Sandboxes and cloud sessions limit what an allowed command can reach.

## Related defaults from the talk

- Run the newest capable model, so you do not steer mid-session.
- Do not use skip-all-permissions as a substitute for auto mode. The talk frames that as the riskier workaround from before auto mode existed.
