#!/usr/bin/env bash
# Example hook: run the whole test suite before a session is allowed to finish.
#
# Intended event: Stop.
# Configure:      ACS_TEST_CMD="npm test --silent"
#                 ACS_MAX_BLOCKS=5   (default) consecutive failures before giving up
# Unset ACS_TEST_CMD -> does nothing (exit 0).
#
# On failure: output to stderr, exit 2, so Claude keeps working instead of finishing.
#
# Our own safety valve (not from the source talk): a counter per session. After
# ACS_MAX_BLOCKS consecutive failures the hook stops blocking, so a suite that can
# never pass cannot trap a session forever. It then exits 0, which means the session
# CAN finish with failing tests. Treat that as a signal to look, and keep CI as the
# real backstop.
set -u
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=_lib.sh
. "$HERE/_lib.sh"

acs_read_input
[ -n "${ACS_TEST_CMD:-}" ] || exit 0

session="$(acs_json_get session_id)"
session="${session:-nosession}"
session="${session//[^A-Za-z0-9_-]/_}"
counter="${TMPDIR:-/tmp}/acs-stop-${session}.count"
max="${ACS_MAX_BLOCKS:-5}"

if output="$(bash -c "$ACS_TEST_CMD" 2>&1)"; then
  rm -f "$counter"
  exit 0
fi

count=0
[ -f "$counter" ] && count="$(cat "$counter" 2>/dev/null || echo 0)"
count=$((count + 1))
printf '%s' "$count" > "$counter"

if [ "$count" -gt "$max" ]; then
  rm -f "$counter"
  printf '%s\n' "full-suite-on-stop: tests still failing after $max blocks; allowing stop. Check CI." >&2
  exit 0
fi

acs_fail "Test suite is failing (attempt $count of $max). Fix it before finishing:
$output"
