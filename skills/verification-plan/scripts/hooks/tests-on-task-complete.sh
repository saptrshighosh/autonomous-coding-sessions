#!/usr/bin/env bash
# Example hook: run the tests for what changed before a task may be marked complete.
#
# Intended event: TaskCompleted (confirm the event name in the current hooks docs).
# Configure:      ACS_TASK_TEST_CMD="pytest tests/auth"
#                 Point it at whatever is scoped to the work, e.g. a script that maps
#                 changed files to test paths. This repo does not guess that mapping.
# Unset ACS_TASK_TEST_CMD -> does nothing (exit 0).
#
# On failure: output to stderr, exit 2, which blocks completion and sends Claude back.
set -u
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=_lib.sh
. "$HERE/_lib.sh"

acs_read_input
[ -n "${ACS_TASK_TEST_CMD:-}" ] || exit 0

if output="$(bash -c "$ACS_TASK_TEST_CMD" 2>&1)"; then
  exit 0
fi
acs_fail "Task tests failed, so the task is not complete:
$output"
