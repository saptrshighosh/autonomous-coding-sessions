# 04. Keeping sessions safe

Upgrading the model and using auto mode only means you are working with a model. It usually does what you tell it, but that is not a guarantee. A guarantee can only be enforced in the harness or the environment.

## Why not rely on the model or on you

The talk cites a study Anthropic published in August that compared auto mode with real people in the loop:

- About **14%** of people caught a clearly dangerous command.
- Auto mode blocked about **89%** of them.
- So auto mode is far better than a human at this, but roughly **1 in 10** still went through.

(Reported as stated in the talk. We have not re-run or independently verified the study.)

## Layer 1: deny rules (harness)

- A tool call that matches a deny rule is checked before the auto mode classifier. If it matches, the classifier never sees it.
- Deny rules are therefore the strongest way to be sure Claude never does something.
- They live in the project, so commit them. Cloud sessions then get them too.

### Deciding what must be a rule

Ask: **if Claude gets this wrong once, can I take it back?**

| Situation | Reversible? | Treatment |
|---|---|---|
| Wrote the wrong code | Yes, revert it | Leave it to the model |
| Discarded uncommitted changes | No | Rule |
| Read a secret that is now in the transcript | No | Rule |
| Pushed to a deploy repo | Depends on blast radius | Auto mode policy, rule if risky |

Worked example: you never want Claude reading `.env`. Auto mode alone would approve it. Add a deny rule for that file and, per the talk, commands like `cat` cannot open it either. (Check that claim against the current docs and test it, see `docs/HONEST-LIMITS.md`.)

## Layer 2: sandbox (environment, your own machine)

**The gap.** Permissions only decide whether a tool call runs. They cannot limit what it can reach once it is running.

Example: `npm test` is a normal command, so auto mode allows it. But it runs code you did not write (your dependencies), or a script Claude wrote on the spot. If one of those is compromised it could open `.env` or your SSH keys and send them to a server you have never heard of. A human approving every command would also have clicked allow, because the visible command is harmless.

You cannot just block `npm test`, because running tests is how Claude checks its own work. So limit the side effects instead:

- The sandbox lets you control which files a command can read, which folders it can write, and which hosts it can reach.
- The operating system enforces it, including for every child process the command starts.
- A deny rule alone is checked by Claude on the command text (`npm test`), which does not reveal which files the script opens. With the sandbox on, the same rule is passed to the operating system, so a dependency that tries to open `.env` is refused.
- By default the sandboxed command can still read most of your machine, so add a rule for things like your SSH keys.
- Unapproved hosts are unreachable.

**Limits of the sandbox.** It covers only the shell commands Claude runs and what they start. Claude's own file tools, your MCP servers, and your hooks still run outside it, on your machine, next to everything else on it.

## Layer 3: cloud session (strongest isolation)

Best for long runs, because none of your machine is there at all.

- It gets its own machine with a fresh copy of the repo, and keeps running when you close your laptop.
- `.env`, SSH keys and your GitHub token are not in git, so they are not there.
- If an API key is needed, add it as a network secret. Claude is told mid-session that it is missing, and the key can be used without ever being sent to the model.
- Network access defaults to a short list (package registries and GitHub). Explicitly add any other domain the task needs.

**The disposable machine, durable effects.** The machine is thrown away but what leaves it is not: a commit, a push, or a message goes out through a connector. Keep auto mode on and commit your deny rules into the repo so they come along. They can still catch things like a force push or a secret in a commit.

## Choosing a layer

| Question | Answer points to |
|---|---|
| Must this never happen, whatever the model thinks? | Deny rule |
| Is the risk inside a command that must be allowed (tests, installs, scripts)? | Sandbox, or a cloud session |
| Will it run for hours or while the laptop is closed? | Cloud session |
| Are secrets or SSH keys on the machine at all? | Cloud session removes them |
| Does the effect leave the machine (push, message)? | Deny rules + auto mode + CI, because the environment cannot undo it |

Use `templates/deny-rules.settings.json` as a starting point and the `autonomy-audit` skill to check what a project currently has.
