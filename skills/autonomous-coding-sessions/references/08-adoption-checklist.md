# 08. Adoption checklist

## The talk's recommended first experiment

1. Take **one thing that is way bigger** than you would normally give Claude.
2. Make sure your **CI actually catches the things you care about**.
3. Spend a bit of time **configuring the environment**: its network access, its secrets, and its setup script.
4. **Start in the cloud.**
5. Watch **where your sessions get stuck and where you are still in the loop.** That is the next thing to hand over to Claude.

## A ladder to climb in order

This is the talk's own progression, laid out as stages. Do not skip a stage. Each one makes the next one safe.

| Stage | You have | Skill reference |
|---|---|---|
| 0. Defaults | A current model, auto mode | `01`, `03` |
| 1. Lean instructions | CLAUDE.md with only the invisible facts | `02` |
| 2. Hard limits | Deny rules for irreversible actions, committed in the repo | `04` |
| 3. Contained | Sandbox, or better a cloud session with a network allowlist and secrets handled | `04` |
| 4. Verified | Pass/fail checkpoints; hooks with exit 2 for the ones that must run | `05` |
| 5. Parallel | Several sessions, CI as the backstop, auto-fix | `06` |
| 6. Risk-tiered review | Fresh-context reviewer; humans scaled to risk; merge-when-ready only where safe | `06` |
| 7. Orchestrated | One main session starting and verifying threads | `07` |

## Using the stuck-points log

During step 5 of the experiment, keep a short list. For every time you had to step in, write down:

- what you did (approved something, corrected something, reran something),
- which of the five jobs it was (steer, approve, restrict, check, start),
- what could take it over (model, harness, environment) and whether you can set that up.

Repeat. The list shrinks as the system takes over more of it, and what remains is the work only you should be doing.

## Quick self-check before leaving a session unattended

- [ ] Irreversible actions are covered by deny rules in the repo.
- [ ] Secrets are not reachable (cloud session or sandbox rules).
- [ ] Network access is an explicit list.
- [ ] "Done" is defined as checks that return pass or fail.
- [ ] Hooks that must run exit 2 on failure.
- [ ] CI covers the behavior you care about.
- [ ] You know who or what reviews the result, and how deeply for this risk level.
