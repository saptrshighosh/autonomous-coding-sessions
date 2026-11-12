# Evals

Test cases for the skills in this repo. **No eval has been run and no results are published.** This folder defines what a good answer looks like; it does not claim the skills achieve it.

## What is here

| Path | What it is |
|---|---|
| `<case-name>/prompt.md` | A realistic user prompt, with a settings block for the runner |
| `<case-name>/case.yaml` | The case name and a description of a good result |
| `<case-name>/graders/NN-*.md` | One checkable statement per file, judged against the transcript |
| `trigger-queries.json` | 20 queries (10 should trigger the core skill, 10 near-misses should not) for tuning the skill description |

The six cases cover: mapping human jobs to what takes over, deny rule versus model judgment, `npm test` side effects, the hook exit-code gotcha, trimming a bloated `CLAUDE.md`, and merge-when-ready by risk tier.

The layout is the one read by `claude plugin eval` (Claude Code 2.1.269 or later, per the skill-creator reference). Each case runs with and without the skill, so the honest comparison is skill versus no skill. These are real, billed model runs.

## Running them

```bash
claude plugin eval . --allow-tools Bash,Read,Glob,Grep,Skill
```

Confirm the flags with `claude plugin eval --help` on your version. Output goes to `evals/results/`, which is gitignored on purpose.

## If you publish numbers

- Say the model, Claude Code version, number of runs, and date.
- Publish the raw outputs beside the score. Three or six cases is a smoke test, not a benchmark.
- Add a row to `docs/HONEST-LIMITS.md` that says what was and was not measured.
- Do not edit a grader to make a result pass.

`tests/verify_repo.py` fails if `evals/results/` or `evals/snapshots/` is committed. That guard exists so no figure appears here without raw data behind it.

## Known weaknesses of these cases

- Graders are judged by a model against the transcript, so they can be wrong in both directions.
- Several graders check for the presence of an idea, so a vague answer that mentions it in passing could pass.
- The cases test knowledge from one talk. They do not test whether the audit script or hooks work (that is `tests/`).
