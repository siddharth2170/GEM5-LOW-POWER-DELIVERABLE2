#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
mkdir -p "$ROOT/build"
for src in "$ROOT"/benchmarks/*.c; do
  name="$(basename "$src" .c)"
  gcc -O2 -static -fno-tree-vectorize -fno-unroll-loops "$src" -o "$ROOT/build/$name"
done
file "$ROOT"/build/*
echo "WORKLOAD BUILD COMPLETE"

