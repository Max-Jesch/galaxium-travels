#!/bin/bash
# Convenience wrapper — runs the full e2e test suite from the repo root.
#
#   ./test.sh                              # full run
#   E2E_RUN_SLOW=1 ./test.sh              # include the ~90s auto-expiry test
#   ./test.sh -k confirm                   # pass extra args to pytest

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
exec "${SCRIPT_DIR}/e2e/run-native.sh" "$@"
