# Testing

Everything runs with the Python standard library and bash. No network.

```bash
make check      # verify_repo.py + unit tests + checksum verification
make all        # regenerate synced/generated files first, then check
```

## What each piece covers

| File | Covers |
|---|---|
| `tests/test_audit_setup.py` | Every audit finding against the bad fixture and the hardened example; edge cases (invalid JSON, empty dir, `.env` handling); that the audit never modifies the project; CLI exit codes and JSON output |
| `tests/test_hooks.py` | The three hook scripts as real subprocesses: unset env does nothing, pass exits 0, fail exits **2 and never 1**, malformed stdin, the stop retry cap, per-session counters, hostile session ids, and that the example project's hook copies are identical |
| `tests/test_install_and_package.py` | `install.sh` into temp dirs (install, list, uninstall touches only its own skills, never edits settings); packaging is reproducible and matches the committed archive |
| `tests/test_verify_repo.py` | Runs `verify_repo.py` as part of the suite |
| `tests/verify_repo.py` | Structure and honesty checks (below) |

## What `verify_repo.py` checks

- Required files exist; every JSON file parses.
- Manifests agree: plugin name and version match `gemini-extension.json`, the marketplace entry, `CHANGELOG.md` and `docs/releases/`. `plugin.json` sets no `agents` or `skills` key.
- Skills: exact expected set; name equals folder; valid kebab-case name without "claude" or "anthropic"; description length; no angle brackets; body under 500 lines; a `README.md` beside each; every backticked `references/`, `templates/`, `scripts/` path exists; every reference file is linked from the main `SKILL.md`.
- Agents: exact expected set; no forbidden frontmatter. Commands: no name collides with a skill.
- Evals: every case folder has `prompt.md` (valid settings keys), `case.yaml` (quoted `schema_version`, matching name), and numbered graders; trigger queries have enough positives and negatives; **no results or snapshots are committed**.
- Scripts: `bash -n` on every `.sh`, byte-compile every `.py`, executable bits.
- Example hook copies equal their sources; `CHECKSUMS.sha256` matches; the packaged archive equals a fresh build.
- Every relative Markdown link resolves.
- **Every figure (a number with `%` or thousands separators) in a skill file appears in `docs/PROVENANCE.md`.**

## What is not tested

Skill effectiveness (no eval has been run), hooks inside a live Claude Code session, and GitHub Actions on GitHub. See [Honest limits](../HONEST-LIMITS.md).

## Running the skill evals

`evals/` uses the case-folder layout read by `claude plugin eval` (Claude Code 2.1.269 or later, per the skill-creator reference). Those are real, billed model runs. See `evals/README.md`. If you run them, commit nothing under `evals/results/`, and publish numbers only with the raw outputs beside them.
