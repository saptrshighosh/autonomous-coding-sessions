# Honest limits

What this repo is, what it is not, and what has and has not been tested. Read this before you trust it with anything that matters.

## What it is

A written playbook, compiled from one conference talk, packaged as Claude Code skills, a plugin, two agents, one command, example hook scripts, an audit script, and tests. It is advice and tooling around advice. It is not a runtime, a proxy, or an enforcement layer.

## What has been tested

| Thing | How | Result at release |
|---|---|---|
| `audit_setup.py` | Unit tests against a deliberately bad fixture, a hardened example, and edge cases (invalid JSON, empty directory, read-only behavior, exit codes) | Passing |
| Example hook scripts | Unit tests that run them with real shell commands: pass, fail (exit 2, never 1), unset variables, malformed stdin, retry cap, per-session counters, hostile session ids | Passing |
| `install.sh` | Unit tests against temp directories: install, list, uninstall only its own skills, never touches settings | Passing |
| Skill packaging | The archive is rebuilt byte-for-byte and compared with the committed one | Passing |
| Repo structure | `tests/verify_repo.py`: frontmatter, names, link targets, eval layout, manifest consistency, checksums, "every figure is in PROVENANCE.md" | Passing |

## What has not been tested

- **No skill has been evaluated for effect.** The `evals/` folder holds test cases and graders, plus trigger queries. **No eval has been run, and no results are published.** Whether these skills make Claude's answers better than no skill is unknown. Do not read the existence of the eval cases as evidence of quality.
- **The example hooks have not been run inside a live Claude Code session**, only as standalone scripts fed JSON on stdin. Event names, exit-code semantics and stdin fields come from a third-party guide (see `PROVENANCE.md`), not from the official reference.
- **The auto mode policy text location is unknown.** The talk says it can be written in plain English in settings but not where. `templates/auto-mode-policy.md` therefore has no settings key.
- **GitHub Actions workflows have not run on GitHub.** They were written to mirror the local `make` targets and have only been checked as valid YAML. Action versions are pinned to commit hashes copied from a reference repository's workflows as of 2026-11-12; recheck them.
- **Windows is unsupported.** There is no PowerShell installer, and the shell scripts assume bash and python3.
- **Only Claude Code is targeted.** `GEMINI.md` and `gemini-extension.json` exist as reading material; Gemini CLI behavior was not tested, and the setting names in the skills are Claude Code's. No Cursor, Codex or other agent integrations are provided because their formats were not verified.

## Known uncertainties in the content

1. **The `.env` deny rule and `cat`.** The talk says a deny rule for `.env` also stops `cat`. Other documentation describes read deny rules as covering the built-in file tools, with shell commands covered only by a sandbox. Test it on your version: add the rule, then ask Claude to `cat .env` in a scratch project.
2. **The 14% / 89% / 1 in 10 figures** come from a study the talk cites. We did not read it. The talk gives no sample size or definition.
3. **The command that audits CLAUDE.md against a model** is mentioned in the talk, but the transcript garbled its name. No name is given here.
4. **Model names and product features** (Opus 5.5, Fable, Claude Code projects in beta, auto mode as default since August) are as described in the talk in late 2026 and will age.
5. **Compiler's inferences.** The talk was spoken, not written as a spec. Where we turned an aside into a rule (for example the "can I take it back?" decision table), the underlying heuristic is the talk's but the table form is ours.

## Heuristic checks

The audit script is a set of simple file checks. It can miss real problems (user-level settings, cloud config, branch protection, a CI job that runs nothing useful) and it can flag harmless things (a `NEVER` in a CLAUDE.md that is actually the project's own vocabulary). A clean audit is not a safety certificate.

## Trust model

- No network access: nothing in this repo makes a network request, and the scripts use only the standard library.
- `install.sh` copies skill folders and nothing else. It never edits settings and never registers hooks.
- `CHECKSUMS.sha256` catches accidental or partial changes. It does not prove authorship. Pin to a release tag, and read the diff.
- The skills are instructions that Claude follows. Review them like code before installing, as with any skill.

## How to report a mistake

Open an issue using the "Content correction" template and cite the claim, what you believe is correct, and a source. Corrections that cite sources are merged fastest.
