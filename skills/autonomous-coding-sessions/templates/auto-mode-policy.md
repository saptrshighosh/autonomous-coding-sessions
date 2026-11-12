# Auto mode policy (plain English)

Auto mode reads a plain-English policy and the classifier uses it to allow or reject commands. Fill in the blanks. Keep each line a concrete fact about your environment, not a general wish.

Where this text lives in settings is not stated in the source talk. Look it up in the current Claude Code docs before pasting.

## Trusted

- Repositories: `<org/repo>`, `<org/deploy-repo>` (pushes here are expected)
- Buckets: `<bucket-name>` (read and write)
- Domains: `<api.example.com>`, `<registry.example.com>`

## Always allow

- Running the project's tests and linters
- Installing dependencies from `<your registry>`
- `<other routine commands for this project>`

## Never do

- Force-push to any branch
- Delete or discard uncommitted changes
- Read or print the contents of `.env` files or SSH keys
- `<anything irreversible in your environment>`

## Notes for the author

- "Never" items that must hold even if the classifier errs should also be **deny rules**. Policy text is judged by a classifier; deny rules are checked before it. See `references/04-safety-layers.md`.
- The talk's default: auto mode trusts only the current folder and repo. Everything in "Trusted" extends that.
