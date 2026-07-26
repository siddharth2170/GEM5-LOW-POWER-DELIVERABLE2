# Part 2 Report Template

## Environment

- Host OS:
- gem5 version: 25.1.0.1
- Host CPU/RAM:
- Guest ISA: x86-64
- Mode: syscall emulation
- Clock: 2 GHz
- Cache hierarchy: 32 KiB L1I, 32 KiB L1D, 256 KiB shared L2

## 1. Basic Pipeline Simulation

Insert the configuration-terminal screenshot and a readable excerpt from
`results/pipeline_trace/minor_trace.txt`.

Explain pipeline fill, steady-state overlap, dependencies, stalls, and branch
redirection. Report cycles, committed instructions, IPC, and observed trace
behavior.

## 2. Impact of Branch Prediction

Insert `results/charts/branch_ipc.png` and the three terminal/statistics
screenshots. Copy the relevant rows from `results/summary.csv`.

Discuss how prediction changes front-end continuity, squashes, cycles, IPC, and
branch MPKI. Explain why an inaccurate predictor can waste more work in a wide,
deep pipeline.

## 3. Multiple Issue

Insert `results/charts/issue_ipc.png`. Compare 1-, 2-, and 4-wide runs. Discuss
why speedup is less than proportional to nominal width and identify dependency,
front-end, memory, or execution-resource limits.

## 4. Simultaneous Multithreading

Insert `results/charts/smt_ipc.png`. Compare aggregate IPC and, if present in
`stats.txt`, per-thread committed instructions. Discuss utilization, fairness,
queue/register/cache pressure, and memory contention.

## 5. Interaction, Limitations, and Complexity

Explain how prediction feeds the instruction window, out-of-order issue finds
ready work, superscalar width consumes it, and SMT fills otherwise unused slots.
Balance performance against area, power, design complexity, and security.

## Troubleshooting

Document at least one actual issue, its diagnostic evidence, and the fix.

