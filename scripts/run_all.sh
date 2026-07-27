#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
GEM5="${GEM5_BIN:-$ROOT/gem5/build/X86/gem5.opt}"
CFG="$ROOT/configs/run_experiment.py"
mkdir -p "$ROOT/results"

run() {
  local name="$1"; shift
  local out="$ROOT/results/$name"
  mkdir -p "$out"
  echo "RUNNING $name"
  "$GEM5" -d "$out" "$CFG" "$@" 2>&1 | tee "$out/terminal.txt"
}

# Section 1: X86 in-order timing baseline and a short execution trace.
run pipeline_timing --experiment pipeline --binary "$ROOT/build/ilp_bench" --arg 500000
mkdir -p "$ROOT/results/pipeline_trace"
"$GEM5" -d "$ROOT/results/pipeline_trace" \
  --debug-flags=Exec --debug-file=execution_trace.txt \
  "$CFG" --experiment pipeline --binary "$ROOT/build/ilp_bench" \
  --arg 2000 --maxinsts 5000 2>&1 | tee "$ROOT/results/pipeline_trace/terminal.txt"

# Section 2: branch-prediction comparison.
run branch_minimal --experiment branch --predictor minimal \
  --binary "$ROOT/build/branch_bench" --arg 500000
run branch_local --experiment branch --predictor local \
  --binary "$ROOT/build/branch_bench" --arg 500000
run branch_tournament --experiment branch --predictor tournament \
  --binary "$ROOT/build/branch_bench" --arg 500000

# Section 3: multiple-issue comparison.
for width in 1 2 4; do
  run "issue_w${width}" --experiment issue --width "$width" \
    --binary "$ROOT/build/ilp_bench" --arg 750000
done

# Section 4: one-thread baseline and two-thread SMT.
run smt_1thread --experiment issue --width 4 --binary "$ROOT/build/thread_a"
run smt_2thread --experiment smt --binary "$ROOT/build/thread_a" \
  --binary2 "$ROOT/build/thread_b"

# Low-power design points: static DVFS plus front-/back-end width gating.
for profile in performance balanced eco; do
  run "low_power_${profile}" --experiment low_power \
    --power-profile "$profile" --predictor tournament \
    --binary "$ROOT/build/ilp_bench" --arg 750000
done

echo "ALL SIMULATIONS COMPLETE"
