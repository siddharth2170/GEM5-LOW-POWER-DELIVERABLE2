#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
GEM5="${GEM5_BIN:-$ROOT/gem5/build/X86/gem5.opt}"
test -x "$GEM5"
test -x "$ROOT/build/thread_a"
mkdir -p "$ROOT/results/smoke"
"$GEM5" -d "$ROOT/results/smoke" "$ROOT/configs/hello_world.py" \
  --binary "$ROOT/build/thread_a" 2>&1 | tee "$ROOT/results/smoke/terminal.txt"
grep -q "thread-a=" "$ROOT/results/smoke/terminal.txt"
grep -q "simInsts" "$ROOT/results/smoke/stats.txt"
echo "SMOKE TEST PASSED"
