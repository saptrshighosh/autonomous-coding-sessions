# reversibility-check

A small decision procedure: for each action Claude might take unattended, ask "if Claude gets this wrong once, can I take it back?" and pick the right layer (model, auto mode policy, deny rule, sandbox, or cloud session).

## When to use it

- "Should reading `.env` be a deny rule?"
- "Can I let Claude push to staging on its own?"
- "What should I block before running sessions overnight?"

## What it does not do

It does not write your settings or measure anything. It gives a recommendation and says what to verify. For a scan of what a project already has, use `autonomy-audit`.

The worked examples (wrong code, discarded changes, `.env`, `npm test` side effects, pushing to a deploy repo) come from the source talk. See [`docs/PROVENANCE.md`](../../docs/PROVENANCE.md).

`SKILL.md` is the prompt Claude loads; this file is for people browsing the repo.
