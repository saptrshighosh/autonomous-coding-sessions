---
name: reversibility-check
description: Decide whether an action Claude might take unattended should be left to the model, covered by an auto mode policy, made a deny rule, or contained by a sandbox or cloud session, using the question "if Claude gets this wrong once, can I take it back?". Use when the user asks "should this be a deny rule?", "is it safe to let Claude do X on its own?", "what should I block?", or is deciding what to restrict before running long or parallel sessions.
---

# Reversibility check

One question sorts almost every "should I restrict this?" decision: **if Claude gets this wrong once, can I take it back?**

## Procedure

For each action the user is worried about:

1. **State the action and what is at stake.** Name the concrete thing: a file, a repo, a secret, a deployment.
2. **Ask the question.** Can a single mistake be undone, cheaply?
   - **Yes:** leave it to the model. Wrong code can be reverted, so no rule is needed.
   - **No:** it should be enforced, not trusted. Continue.
3. **Find where the risk sits** and pick the layer:

| Where the risk sits | Layer |
|---|---|
| The action itself must never happen (reading a secret, discarding uncommitted work) | **Deny rule.** Checked before the auto mode classifier, so the classifier never sees a matching call. |
| Inside a command that must stay allowed (tests, installs, scripts run by them) | **Sandbox** (OS-enforced file, folder and host limits, including child processes) or a **cloud session** |
| It runs for hours, or secrets exist on the machine at all | **Cloud session**: fresh repo copy, no `.env`, SSH keys or tokens, network on an allowlist |
| The effect leaves the machine (commit, push, message) | **Deny rules plus auto mode, committed in the repo**, and CI, because the environment cannot undo it |
| It is a routine, trusted action that auto mode blocks by default (for example pushing to a deploy repo) | **Auto mode policy** in plain English: trusted repos, buckets, domains |

4. **Recommend, with one sentence of reasoning.** Do not stack every layer on every action; match the layer to the risk.

## Worked examples from the source talk

| Action | Reversible? | Answer |
|---|---|---|
| Claude writes the wrong code | Yes (revert) | Leave to the model |
| Claude discards uncommitted changes | No | Deny rule |
| Claude reads `.env` and the key lands in the transcript | No | Deny rule on the file; better, run in a cloud session where it does not exist |
| `npm test` runs a compromised dependency that reads `.env` or SSH keys and sends them out | No | Deny rules alone are not enough, because they see only the command text. Sandbox or cloud session |
| Ship to staging by pushing to a separate deploy repo | Depends | Auto mode blocks it by default; add the deploy repo to the trusted list |

## Be honest about the limits

- Auto mode is not a guarantee. In the talk's study it blocked about 89% of clearly dangerous commands, and people in the loop caught about 14%. Roughly 1 in 10 still got through auto mode.
- The claim that a `Read(...)` deny rule also stops `cat` is the talk's. Suggest the user test it on their version, because other docs describe shell commands as covered only by a sandbox.
- Setting names and syntax change; confirm them in the current docs. `templates/deny-rules.settings.json` in the main `autonomous-coding-sessions` skill is a starting point.

## Output shape

```
Action: <what>
Reversible? <yes/no, why>
Recommendation: <layer> because <one sentence>
Caveat: <anything to verify>
```
