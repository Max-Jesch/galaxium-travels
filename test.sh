#!/bin/bash
# Convenience wrapper — runs the full e2e test suite from the repo root.
# See e2e/README.md for options.
#
#   ./test.sh                              # full run (manages docker compose)
#   E2E_RUN_SLOW=1 ./test.sh              # include the ~90s auto-expiry test
#   E2E_BASE_URL=http://localhost:8001 ./test.sh   # run against existing stack
#   ./test.sh -k confirm                   # pass extra args to pytest

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
exec "${SCRIPT_DIR}/e2e/run.sh" "$@"
