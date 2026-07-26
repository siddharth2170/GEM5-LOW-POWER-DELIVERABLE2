# Phase 2 — Low-Power Microprocessor Implementation with gem5

This repository contains the implementation and report for Deliverable 2. It
runs five reproducible gem5 experiment groups:

1. Basic pipeline behavior with `MinorCPU`
2. Branch prediction using a minimal 1-bit baseline, `LocalBP`, and `TournamentBP`
3. Single-, dual-, and four-wide out-of-order issue
4. One-thread versus two-thread SMT
5. Low-power operating points combining static DVFS and pipeline-width gating

The low-power profiles are:

- `performance`: 2.0 GHz, 1.0 V, four-wide
- `balanced`: 1.6 GHz, 0.9 V, two-wide
- `eco`: 1.2 GHz, 0.8 V, one-wide

The project is pinned to gem5 **v25.1.0.1** and uses x86 syscall-emulation
(SE) mode. It creates separate output directories, extracts common statistics,
and generates CSV summaries and PNG charts.

## Recommended environment

- Docker Desktop on macOS, Windows, or Linux
- 8 GB RAM minimum; 16 GB recommended
- 25 GB free disk space
- 4 or more CPU threads

The Docker image runs Ubuntu 24.04 x86-64 and is suitable for Intel and Apple
Silicon Macs. Apple Silicon uses Docker's x86-64 emulation and will run more
slowly.

## Quick start

```bash
cd gem5-low-power-deliverable2
chmod +x scripts/*.sh
./scripts/docker_build.sh
./scripts/docker_smoke_test.sh
./scripts/docker_run_all.sh
```

Do **not** run `setup_ubuntu.sh` directly on macOS. It is retained only for
people already using an Ubuntu host.

Detailed commands, expected output, and the required screenshot list are in
[`docs/SETUP_AND_SCREENSHOTS.md`](docs/SETUP_AND_SCREENSHOTS.md).

The completed implementation guide is
[`Gem5_Deliverable_2_Implementation_Guide.docx`](Gem5_Deliverable_2_Implementation_Guide.docx).

## Repository layout

```text
benchmarks/       Small deterministic C workloads
configs/          gem5 configuration scripts
scripts/          Setup, build, and experiment runners
analysis/         Statistics parser and chart generator
docs/             Submission and screenshot instructions
Dockerfile        Reproducible Ubuntu/gem5 environment
compose.yaml      Docker service and bind-mounted workspace
build/            Compiled workloads (generated)
results/          gem5 outputs, CSV files, and charts (generated)
```

## Academic integrity

The scripts generate measurements on your machine. Do not submit the empty
example tables or another person's values. Preserve the terminal commands,
`stats.txt` files, and screenshots that correspond to your own run.

## Official references

- gem5 documentation: https://www.gem5.org/documentation/
- gem5 repository/releases: https://github.com/gem5/gem5
- MinorCPU model: https://www.gem5.org/documentation/general_docs/cpu_models/minor_cpu
