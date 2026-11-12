# 07. Orchestrating sessions

## Why

If you are like most people, switching context across many sessions at once goes badly. The direction described in the talk, which Anthropic was already doing more of, is that you no longer start every session yourself.

## The shape

- You keep **one main session**, the orchestrator.
- You tell it what needs to be done.
- It splits the work, starts a new session ("thread") for each task, keeps track of what comes back, and verifies it.
- If something comes back that is not actually done, it sends it back until it is done and passes everything.
- You talk to one session instead of, say, eight.

The talk points to Claude Code projects (still in beta at the time) as an example of this.

## Two roles, two models

| Role | Does | Model should be good at |
|---|---|---|
| Orchestrator (main session) | Decides what to do, judges what comes back. Does **not** write the code. | Deciding and judging. The talk names Fable as an example. |
| Threads (worker sessions) | Do the actual work | Doing the work. The talk names Opus 5.5 as an example. |

The two can be set separately.

## Context management

With Claude Code projects specifically, context is managed for you: no deciding when to compact or clear.

## What stays human

You start the first session and review what comes out. Everything before that (checkpoints, hooks, CI) is what makes it reasonable to be absent. An orchestrator without those just delegates the same unverified work in parallel.

## When not to bother

A single script or a small change does not need an orchestrator. Add this layer when you find yourself managing several sessions by hand and losing track of them.
