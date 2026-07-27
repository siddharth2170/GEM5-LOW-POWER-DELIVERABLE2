#!/usr/bin/env python3
import csv
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
RUNS = [
    "pipeline_timing", "branch_minimal", "branch_local", "branch_tournament",
    "issue_w1", "issue_w2", "issue_w4", "smt_1thread", "smt_2thread",
    "low_power_performance", "low_power_balanced", "low_power_eco",
]

LOW_POWER = {
    "low_power_performance": (2.0, 1.0, 4),
    "low_power_balanced": (1.6, 0.9, 2),
    "low_power_eco": (1.2, 0.8, 1),
}

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
    ghz, volts, width = LOW_POWER.get(name, (None, None, None))
    power_proxy = (
        (volts / 1.0) ** 2 * (ghz / 2.0) * (width / 4.0)
        if ghz is not None else None
    )
    rows.append({
        "run":name, "instructions":insts, "cycles":cycles, "sim_ticks":ticks,
        "ipc":ipc, "branch_lookups":bp_lookups,
        "branch_mispredictions":bp_misses, "branch_mpki":mpki,
        "clock_ghz":ghz, "voltage_v":volts, "pipeline_width":width,
        "normalized_power_proxy":power_proxy,
        "normalized_time":None, "normalized_energy_proxy":None,
    })

perf = next((r for r in rows if r["run"] == "low_power_performance"), None)
if perf and perf["sim_ticks"]:
    for row in rows:
        if row["run"] in LOW_POWER and row["sim_ticks"]:
            row["normalized_time"] = row["sim_ticks"] / perf["sim_ticks"]
            row["normalized_energy_proxy"] = (
                row["normalized_power_proxy"] * row["normalized_time"]
            )

RESULTS.mkdir(exist_ok=True)
out=RESULTS/"summary.csv"
with out.open("w",newline="") as f:
    w=csv.DictWriter(f,fieldnames=rows[0].keys() if rows else
        ["run","instructions","cycles","sim_ticks","ipc","branch_lookups",
         "branch_mispredictions","branch_mpki","clock_ghz","voltage_v",
         "pipeline_width","normalized_power_proxy","normalized_time",
         "normalized_energy_proxy"])
    w.writeheader(); w.writerows(rows)
print(out)
for row in rows: print(row)
