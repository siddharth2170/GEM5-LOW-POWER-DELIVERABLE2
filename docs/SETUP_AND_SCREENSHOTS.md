# Setup, Run, and Screenshot Guide

## 1. Create the Docker environment

Install and start Docker Desktop. On macOS, wait until its menu-bar icon reports
that the engine is running. Then open Terminal:

```bash
unzip ilp-gem5-part2.zip
cd ilp-gem5-part2
chmod +x scripts/*.sh
docker --version
docker compose version
./scripts/docker_build.sh
```

The image contains Ubuntu 24.04 x86-64, the official gem5 v25.1.0.1 release,
an isolated Python virtual environment, and the required compiler tools. The
first image build can take 20–90 minutes. Apple Silicon runs this x86-64 image
through emulation and is normally slower.

Do not run `./scripts/setup_ubuntu.sh` in macOS Terminal. `apt-get` is an Ubuntu
package manager and exists only inside the container.

**Screenshot 1:** Terminal showing Docker and Compose versions, followed by
`DOCKER IMAGE READY`.

Confirm the version:

```bash
docker compose run --rm ilp gem5.opt --version
```

**Screenshot 2:** The gem5 version output.

## 2. Compile and verify workloads

```bash
./scripts/docker_smoke_test.sh
```

**Screenshot 3:** `file` output identifying the benchmarks as statically linked
x86-64 Linux executables.

**Screenshot 4:** Smoke-test terminal showing the checksum, gem5 exit cause, and
`SMOKE TEST PASSED`.

## 3. Section 1 — Basic pipeline

```bash
docker compose run --rm ilp bash -lc \
  './scripts/build_workloads.sh && ./scripts/run_section.sh pipeline'
```

The main output is `results/pipeline_timing/`; the instruction trace is
`results/pipeline_trace/execution_trace.txt`.

```bash
head -n 35 results/pipeline_trace/execution_trace.txt
grep -E "simInsts|numCycles|ipc" results/pipeline_timing/stats.txt
```

**Screenshot 5:** Terminal showing the pipeline configuration and completion.

**Screenshot 6:** A readable execution-trace excerpt from the X86 in-order
timing baseline.

**Screenshot 7:** Pipeline statistics (`simInsts`, cycles, and IPC if present).

## 4. Section 2 — Branch prediction

```bash
docker compose run --rm ilp bash -lc \
  './scripts/build_workloads.sh && ./scripts/run_section.sh branch && python analysis/parse_stats.py && python analysis/make_charts.py'
```

Inspect:

```bash
grep -E "simInsts|numCycles|branchPred.*(lookups|Incorrect|mispred)" \
  results/branch_*/stats.txt
```

**Screenshot 8:** Commands completing all three predictor configurations.

**Screenshot 9:** Relevant branch-predictor statistics.

**Screenshot 10:** Open `results/charts/branch_ipc.png`.

The O3 CPU requires a non-null predictor. Therefore, `branch_minimal` is a
deliberately tiny eight-entry, one-bit local predictor used as the
prediction-minimized baseline. Label the experiment “minimal/simple versus
advanced prediction”; do not claim that the O3 core literally has no predictor.

## 5. Section 3 — Multiple issue

```bash
docker compose run --rm ilp bash -lc \
  './scripts/build_workloads.sh && ./scripts/run_section.sh issue && python analysis/parse_stats.py && python analysis/make_charts.py'
```

```bash
grep -E "simInsts|numCycles|ipc" results/issue_w*/stats.txt
```

**Screenshot 11:** Completion of the 1-, 2-, and 4-wide runs.

**Screenshot 12:** The extracted statistics.

**Screenshot 13:** Open `results/charts/issue_ipc.png`.

## 6. Section 4 — SMT

```bash
docker compose run --rm ilp bash -lc \
  './scripts/build_workloads.sh && ./scripts/run_section.sh smt && python analysis/parse_stats.py && python analysis/make_charts.py'
```

```bash
grep -E "simInsts|numCycles|committedInsts|ipc" results/smt_*/stats.txt
```

**Screenshot 14:** One-thread and SMT terminal completions.

**Screenshot 15:** Aggregate and per-thread statistics.

**Screenshot 16:** Open `results/charts/smt_ipc.png`.

## 7. Final evidence and submission

```bash
column -s, -t results/summary.csv
find results -maxdepth 2 -type f | sort
```

**Screenshot 17:** The formatted summary table.

**Screenshot 18:** The results file listing, proving that each run has a
separate `stats.txt`, `config.ini`, `config.json`, and terminal log.

Copy numerical results into `docs/REPORT_TEMPLATE.md`, insert screenshots, and
include a GitHub repository link. Do not screenshot only charts: retain the
terminal command, configuration identity, and raw statistics as evidence.

To run every section in one command:

```bash
./scripts/docker_run_all.sh
```

## Troubleshooting

- `gcc: cannot find -lc`: install static libc support (`sudo apt install
  libc6-dev`) or use the provided Ubuntu environment.
- `Exec format error`: the benchmark ISA does not match the X86 gem5 build.
- Missing `stats.txt`: inspect the corresponding `terminal.txt` for a fatal
  configuration error.
- Empty chart: rerun the simulations and parser; verify that
  `results/summary.csv` contains nonblank IPC values.
- Build killed: increase VM RAM or reduce `-j$(nproc)` in
  `scripts/setup_ubuntu.sh` to `-j2`.
- `apt-get: command not found` on macOS: you ran the Ubuntu-host script outside
  Docker. Use `./scripts/docker_build.sh`.
- `Cannot connect to the Docker daemon`: open Docker Desktop and wait for the
  engine to finish starting.
- `no matching manifest` or architecture warnings: keep
  `platform: linux/amd64` in `compose.yaml`.
