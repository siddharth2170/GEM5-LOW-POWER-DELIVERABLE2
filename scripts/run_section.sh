#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
GEM5="${GEM5_BIN:-$ROOT/gem5/build/X86/gem5.opt}"
CFG="$ROOT/configs/run_experiment.py"
mkdir -p "$ROOT/results"
run() {
  local name="$1"; shift
  mkdir -p "$ROOT/results/$name"
  echo "RUNNING $name"
  "$GEM5" -d "$ROOT/results/$name" "$CFG" "$@" 2>&1 |
    tee "$ROOT/results/$name/terminal.txt"
}
case "${1:-}" in
  pipeline)
    run pipeline_timing --experiment pipeline --binary "$ROOT/build/ilp_bench" --arg 500000
    mkdir -p "$ROOT/results/pipeline_trace"
    "$GEM5" -d "$ROOT/results/pipeline_trace" --debug-flags=Exec \
      --debug-file=execution_trace.txt "$CFG" --experiment pipeline \
      --binary "$ROOT/build/ilp_bench" --arg 2000 --maxinsts 5000 2>&1 |
      tee "$ROOT/results/pipeline_trace/terminal.txt" ;;
  branch)
    for pred in minimal local tournament; do
      run "branch_${pred}" --experiment branch --predictor "$pred" \
        --binary "$ROOT/build/branch_bench" --arg 500000
    done ;;
  issue)
    for width in 1 2 4; do
      run "issue_w${width}" --experiment issue --width "$width" \
        --binary "$ROOT/build/ilp_bench" --arg 750000
    done ;;
  smt)
    run smt_1thread --experiment issue --width 4 --binary "$ROOT/build/thread_a"
    run smt_2thread --experiment smt --binary "$ROOT/build/thread_a" \
      --binary2 "$ROOT/build/thread_b" ;;
  low_power)
    for profile in performance balanced eco; do
      run "low_power_${profile}" --experiment low_power \
        --power-profile "$profile" --predictor tournament \
        --binary "$ROOT/build/ilp_bench" --arg 750000
    done ;;
  *)
    echo "Usage: $0 {pipeline|branch|issue|smt|low_power}"; exit 2 ;;
esac
