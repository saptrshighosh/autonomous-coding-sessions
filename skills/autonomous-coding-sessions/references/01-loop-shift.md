# 01. The shift out of the loop

## What changed

Earlier in the talk's timeline, sessions with an older model looked like this:

- The model stopped sooner, so runs were short.
- People kept correcting it and stacked emphasis into CLAUDE.md ("important", exclamation marks).
- Auto mode did not exist, so people either approved everything by hand or used the riskier skip-all-permissions option.
- One session, or a couple at a time, with a human in the loop for almost every step.

With current models, sessions at Anthropic (as described in the talk) look different:

- Dozens of sessions running at the same time, for hours.
- Sessions verify their own results along the way.
- Sessions orchestrate other sessions.
- The human acts as a manager of sessions, not an operator of one.
- Throughput rose with this. The talk cites an Anthropic blog post reporting about 2,500 changes per day in May and more than 30,000 per day in September. That figure is the talk's citation of a post we have not independently checked.

## The five jobs

Older best practices were mostly about a human doing these:

1. Steering sessions
2. Approving commands
3. Saying no to things or restricting what Claude can do
4. Checking the output
5. Starting the sessions

Wherever you step out of one of these, something else must take over. The talk names the candidates: **the model, the harness, or the environment**.

| Job | Takeover | Notes |
|---|---|---|
| Steering | Model | Newer models understand intent and codebases, so mid-session corrections drop. |
| Approving | Auto mode (harness) | A separate classifier checks anything beyond reading and editing project files. |
| Restricting | Harness rules + environment | Deny rules, sandbox, cloud session. |
| Checking | Tests, hooks, CI | Plus an independent reviewer. |
| Starting | Orchestrator session | One main session starts and verifies the threads. |

The talk's closing summary: the old best practices are all still there, they have moved. Almost everything people used to do is now the model, the harness, or the environment, and the human starts the first session and reviews what comes out.

## The two questions that drive everything

- If I am not approving every command and I run many sessions, how do I keep **quality** high? (see `05-verification-and-hooks.md`, `06-scaling-ci-review.md`)
- If sessions run for hours unsupervised, how do I keep them **safe**? (see `04-safety-layers.md`)

Getting out of the loop is the easy part (use today's defaults: a current model and auto mode). Making it okay that you are gone is the hard part.

## Using this in a conversation

Ask what the user currently approves, corrects, or reviews by hand. Map each item to a row above and state what would replace it. If a row has no replacement, that is the first thing to fix, and it tells you which reference to open next.
