#!/usr/bin/env python3
import csv
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
RUNS = [
    "pipeline_minor", "branch_minimal", "branch_local", "branch_tournament",
    "issue_w1", "issue_w2", "issue_w4", "smt_1thread", "smt_2thread",
]

def read_stats(path):
    stats = {}
    for line in path.read_text(errors="replace").splitlines():
        m = re.match(r"^(\S+)\s+([-+0-9.eE]+)\s*(?:#.*)?$", line.strip())
        if m:
            try: stats[m.group(1)] = float(m.group(2))
            except ValueError: pass
    return stats

def first(stats, exact=(), suffixes=()):
    for k in exact:
        if k in stats: return stats[k]
    for suffix in suffixes:
        vals = [v for k,v in stats.items() if k.endswith(suffix)]
        if vals: return sum(vals)
    return None

rows=[]
for name in RUNS:
    path=RESULTS/name/"stats.txt"
    if not path.exists():
        print(f"SKIP missing {path}")
        continue
    s=read_stats(path)
    insts=first(s, exact=("simInsts",), suffixes=(".committedInsts", ".numInsts"))
    cycles=first(s, suffixes=(".numCycles",))
    ticks=first(s, exact=("simTicks",))
    ipc=(insts/cycles) if insts and cycles else None
    bp_lookups=first(s, suffixes=(".branchPred.lookups", ".branchPred.condPredicted"))
    bp_misses=first(s, suffixes=(".branchPred.condIncorrect", ".branchPred.mispredicted"))
    mpki=(1000*bp_misses/insts) if bp_misses is not None and insts else None
    rows.append({
        "run":name, "instructions":insts, "cycles":cycles, "sim_ticks":ticks,
        "ipc":ipc, "branch_lookups":bp_lookups,
        "branch_mispredictions":bp_misses, "branch_mpki":mpki,
    })

RESULTS.mkdir(exist_ok=True)
out=RESULTS/"summary.csv"
with out.open("w",newline="") as f:
    w=csv.DictWriter(f,fieldnames=rows[0].keys() if rows else
        ["run","instructions","cycles","sim_ticks","ipc","branch_lookups",
         "branch_mispredictions","branch_mpki"])
    w.writeheader(); w.writerows(rows)
print(out)
for row in rows: print(row)
