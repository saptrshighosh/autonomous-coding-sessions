#!/usr/bin/env bash
# Example hook: run a linter on the file Claude just edited.
#
# Intended event: PostToolUse with matcher "Edit|Write".
# Configure:      ACS_LINT_CMD="eslint --max-warnings 0"   (file path is appended)
# Unset ACS_LINT_CMD -> does nothing (exit 0), so installing it cannot break a project.
#
# On failure it prints the linter output to stderr and exits 2. For PostToolUse the
# edit has already happened, so exit 2 surfaces the problem to Claude rather than
# undoing the edit.
set -u
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=_lib.sh
. "$HERE/_lib.sh"

acs_read_input
[ -n "${ACS_LINT_CMD:-}" ] || exit 0

file="$(acs_json_get tool_input.file_path)"
[ -n "$file" ] || exit 0

if output="$(bash -c "$ACS_LINT_CMD \"\$1\"" _ "$file" 2>&1)"; then
  exit 0
fi
acs_fail "Lint failed for $file:
$output"
