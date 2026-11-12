#!/usr/bin/env bash
# Deliberately wrong: failing tests exit 1, so Claude is never sent back to fix them.
if ! python3 -m pytest -q; then
  echo "tests failed"
  exit 1
fi
