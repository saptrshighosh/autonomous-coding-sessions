# autonomous-coding-sessions

**Unofficial, community-written playbook for running Claude Code with little supervision, without losing safety or quality.**

When you stop approving every command and start running many long sessions at once, something else has to do the jobs you used to do. This repo gives Claude (and you) that map, plus a few small tools to check it.

> Not affiliated with or endorsed by Anthropic. Compiled from one public conference talk by the Claude Code team. **Untested for effect; read [`docs/HONEST-LIMITS.md`](docs/HONEST-LIMITS.md) before you rely on it.**

## The idea in one table

| A human used to... | Now something else does it | In this repo |
|---|---|---|
| Steer the session | The model (current version, short CLAUDE.md) | `autonomous-coding-sessions` |
| Approve every command | Auto mode, plus deny rules for things that must never happen | `reversibility-check` |
| Restrict what is possible | Sandbox or a cloud session | `autonomous-coding-sessions` |
| Check the output | Pass/fail checkpoints, hooks, CI, a fresh-context reviewer | `verification-plan` |
| Start sessions | An orchestrator session | `autonomous-coding-sessions` |

## Before and after

You ask: *"Is it safe to let Claude run `npm test` on its own if I've blocked `.env` reads?"*

| Without the skill (typical) | With `reversibility-check` |
|---|---|
| "Yes, the deny rule stops it reading `.env`." | "Not fully. A permission decides whether `npm test` runs, not what the code it starts can reach. A compromised dependency could still read other files and send them out. Contain it with a sandbox, or run in a cloud session where those secrets don't exist." |

That example is the kind of answer the skills aim for. It is illustrative, not a measured result.

## Install

```bash
# Claude Code plugin (after you publish or fork this repo to GitHub)
/plugin marketplace add saptrshighosh/autonomous-coding-sessions
/plugin install autonomous-coding-sessions@autonomous-coding-sessions

# Or copy the skills into your personal skills folder
git clone https://github.com/saptrshighosh/autonomous-coding-sessions
cd autonomous-coding-sessions && ./install.sh
```

Full matrix and uninstall: [`INSTALL.md`](INSTALL.md).

## What you get

| Piece | What it is |
|---|---|
| `autonomous-coding-sessions` skill | The core playbook: eight reference topics and four templates |
| `autonomy-audit` skill | A read-only script that checks your `CLAUDE.md`, settings, hooks and CI, then explains each finding |
| `reversibility-check` skill | "If Claude gets this wrong once, can I take it back?" turned into a decision procedure |
| `verification-plan` skill | Pass/fail checkpoints, and three opt-in hook scripts that exit 2 on failure |
| `autonomy-auditor`, `fresh-context-reviewer` agents | Read-only auditor and independent reviewer |
| `/stuck-points` command | Log where you are still in the loop and pick what to hand over next |
| `examples/hardened-project` | A fake project the audit passes |

## Honest by design

- Every figure in a skill must appear in [`docs/PROVENANCE.md`](docs/PROVENANCE.md), or `make check` fails.
- No eval results are published, because none were run. See [`evals/README.md`](evals/README.md).
- The hook scripts are unit-tested as real subprocesses, but have **not** been run in a live Claude Code session.
- Hook event names came from a third-party guide, not the official reference. The talk's claim that a `Read` deny rule also blocks `cat` is flagged for you to test.

## Develop

```bash
make all      # regenerate synced files, rebuild the archive and checksums, then verify
make check    # verify + unit tests + checksum check
```

See [`CONTRIBUTING.md`](CONTRIBUTING.md) and [`docs/README.md`](docs/README.md).

## License

MIT, see [`LICENSE`](LICENSE). "Claude" and "Anthropic" are trademarks of Anthropic, PBC; see [`TRADEMARKS.md`](TRADEMARKS.md).
