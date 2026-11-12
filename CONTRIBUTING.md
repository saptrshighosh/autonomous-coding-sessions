# Contributing

Corrections and improvements are welcome, especially ones that cite a source.

## Good contributions

- Fixing a claim that is wrong, with a link to the official docs or the talk.
- Testing an uncertain claim on your version and reporting the result (see `docs/HONEST-LIMITS.md`, "Known uncertainties").
- Running the evals and sharing raw results (see `evals/README.md`).
- Better hook scripts, audit checks, or examples, with tests.
- Clearer wording in the references.

## Before you open a PR

```bash
make all
```

That regenerates the synced example hooks, the packaged archive and the checksums, then runs the verifier and all tests. CI runs the same checks.

- **Tests:** add a test for any new script behavior. Hooks must exit 2 on failure, never 1.
- **Provenance:** any new figure needs a row in `docs/PROVENANCE.md` first. Any new unverified claim goes in `docs/HONEST-LIMITS.md`.
- **Generated files go in the same PR as their source.** Do not hand-edit `dist/`, `CHECKSUMS.sha256`, or the copies under `examples/hardened-project/.claude/hooks/`.
- **Keep it small and focused.** One idea per PR.
- **Match the surroundings.** Plain language, short files, no emphasis shouting.

## What a maintainer checks

License scope, tests, generated files, honesty (no invented numbers, syntax, or results), and security boundaries: scripts stay read-only or opt-in, and nothing registers a hook or edits settings on its own.

## Licensing of contributions

The repo is MIT licensed (see `LICENSE`). By contributing you agree your contribution is under the same license. Do not paste text from other projects or from the source talk's transcript beyond short quotations.

## Questions

Open a discussion or an issue. Use the "Content correction" template for factual fixes.
