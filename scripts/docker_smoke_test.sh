#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
docker compose run --rm ilp bash -lc \
  './scripts/build_workloads.sh && ./scripts/smoke_test.sh'

