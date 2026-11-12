# Security

This repo contains instructions for an AI model, a few shell and Python scripts, and example configuration. It makes no network requests and runs nothing on its own.

## What could go wrong

| Surface | Risk | Mitigation |
|---|---|---|
| Skills (`SKILL.md`, references) | A malicious or careless edit could steer Claude toward unsafe actions | Review them like code before installing; pin to a release tag; `docs/PROVENANCE.md` records the origin of every claim |
| `install.sh` | Copying files into your skills folder | Copies four named folders and nothing else; never edits settings or registers hooks; `--list` shows what it will do; unit-tested |
| Hook scripts (opt-in) | They run commands you configure on every matching event | They do nothing unless you set an `ACS_*` variable; they run exactly the command you set, with no network use of their own; session ids are sanitized before use in a path |
| `audit_setup.py` | Reads project files | Read-only and standard library only; a test checks it never modifies the audited directory |
| Example settings and policy text | Copied into a real project, giving false confidence | They are starting points. `docs/HONEST-LIMITS.md` lists what is unverified |

## Not a security guarantee

Advice in this repo can be wrong or out of date. Auto mode, deny rules, sandboxes and cloud sessions each have limits, and the references say so. A clean audit means nothing was found on disk, not that a setup is safe.

## Supported versions

Only the latest release.

## Report a vulnerability

Please use GitHub's private vulnerability reporting for this repository (Security tab, "Report a vulnerability") rather than a public issue, for anything like a script that can be made to run unintended commands, a path escape, or an installer that touches files it should not. Include the file, the input that triggers it, and what you expected.

Response targets for a volunteer project: acknowledgement within a week, a fix or mitigation for a confirmed serious issue as soon as practical. These are goals, not a contractual SLA.

## Verifying a download

`CHECKSUMS.sha256` lists SHA-256 digests for scripts, manifests, the installer, example hooks and the packaged skill. `python3 scripts/gen_checksums.py --check` verifies them. This catches accidental or partial changes, not a malicious tag, so read the diff between releases.
