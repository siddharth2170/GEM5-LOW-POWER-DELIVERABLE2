#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
sudo apt-get update
sudo apt-get install -y build-essential git scons python3 python3-venv \
  python3-dev pkg-config m4 zlib1g zlib1g-dev libprotobuf-dev protobuf-compiler \
  libprotoc-dev libgoogle-perftools-dev libboost-all-dev libhdf5-dev \
  libpng-dev
if [[ ! -d gem5/.git ]]; then
  git clone --branch v25.1.0.1 --depth 1 https://github.com/gem5/gem5.git
fi
python3 -m venv .venv
./.venv/bin/pip install --upgrade pip
./.venv/bin/pip install -r requirements.txt
cd gem5
scons build/X86/gem5.opt -j"$(nproc)"
echo "SETUP COMPLETE: $ROOT/gem5/build/X86/gem5.opt"
