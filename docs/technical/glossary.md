# Glossary

Terms as used in this playbook.

| Term | Meaning |
|---|---|
| **In the loop** | A human steers, approves, checks or starts each step. Autonomous setups move those jobs elsewhere. |
| **The five jobs** | Steer, approve, restrict, check, start: what a human does in the loop. |
| **Harness** | The Claude Code application around the model: permissions, auto mode, hooks, tools. |
| **Environment** | Where commands run: your machine, a sandbox, or a cloud session. |
| **Auto mode** | A permission mode that runs a separate classifier on nearly everything that is not reading or editing project files, allowing safe commands and blocking unsure ones. |
| **Classifier** | The separate check auto mode uses to allow or block a command. |
| **Deny rule** | A rule that blocks matching tool calls. Checked before the classifier, so a matching call never reaches it. |
| **Sandbox** | OS-enforced limits on which files a command can read, which folders it can write, and which hosts it can reach, including child processes. Covers shell commands only. |
| **Cloud session** | A session on its own machine with a fresh repo copy; runs with your laptop closed; secrets not in git are absent. |
| **Network secret** | A credential added to a cloud session's environment so Claude can use it without it being sent to the model. |
| **Connector** | How a cloud session's commits, pushes and messages leave the disposable machine. |
| **Checkpoint** | A pass/fail check (tests, build, screenshot) used to verify work without reading every change. |
| **Hook** | A script Claude Code runs at a specific point (for example after an edit, when a task completes, when the session wants to finish). |
| **Exit code 2** | The hook exit code that sends Claude back to fix a failure. Exit 1 does not. |
| **CI auto-fix** | Claude sees a failed CI check on a PR and goes back to fix it. |
| **Merge when ready** | The PR merges automatically once all checks pass. Not a default; depends on risk. |
| **Fresh-context review** | Reviewing a change with a session that did not write it and carries none of its context. |
| **Orchestrator** | One main session that splits work, starts worker sessions, tracks and verifies results, and does not write code itself. |
| **Thread** | A worker session started by an orchestrator for one task. |
| **Claude Code projects** | A feature, in beta at the time of the talk, in which an orchestrator manages threads and context automatically. |
| **Reversible** | A mistake that one revert or retry can undo. The test for whether something needs a rule. |
