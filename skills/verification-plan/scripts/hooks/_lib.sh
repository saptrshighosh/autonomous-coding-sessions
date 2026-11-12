# shellcheck shell=bash
# Shared helpers for the example hooks. Sourced, never executed directly.
#
# Hooks receive a JSON object on stdin. We read it once into INPUT and pull
# fields out with python3 (standard library only) so we do not depend on jq.

acs_read_input() {
  INPUT="$(cat 2>/dev/null || true)"
}

# acs_json_get "tool_input.file_path"  -> prints the value, or nothing.
acs_json_get() {
  printf '%s' "${INPUT:-}" | python3 -c '
import json, sys
try:
    node = json.load(sys.stdin)
    for key in sys.argv[1].split("."):
        node = node[key]
except Exception:
    sys.exit(0)
if isinstance(node, bool):
    print("true" if node else "false")
elif isinstance(node, (str, int, float)):
    print(node)
' "$1"
}

# acs_fail "message"  -> message to stderr (shown to Claude), exit code 2.
# Exit code 2, not 1, is what sends Claude back to fix the problem.
acs_fail() {
  printf '%s\n' "$1" >&2
  exit 2
}
