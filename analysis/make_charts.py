#!/usr/bin/env python3
import csv
from pathlib import Path
import matplotlib.pyplot as plt

ROOT=Path(__file__).resolve().parents[1]
RESULTS=ROOT/"results"
rows={r["run"]:r for r in csv.DictReader((RESULTS/"summary.csv").open())}
CHARTS=RESULTS/"charts"; CHARTS.mkdir(exist_ok=True)

def value(run,key):
    raw=rows.get(run,{}).get(key,"")
    return float(raw) if raw not in ("",None,"None") else 0.0

def bar(names, labels, key, title, ylabel, filename):
    vals=[value(n,key) for n in names]
    fig,ax=plt.subplots(figsize=(8,4.8))
    bars=ax.bar(labels,vals,color=["#4472C4","#70AD47","#ED7D31","#A5A5A5"][:len(vals)])
    ax.set_title(title); ax.set_ylabel(ylabel); ax.grid(axis="y",alpha=.25)
    for b,v in zip(bars,vals): ax.text(b.get_x()+b.get_width()/2,v,f"{v:.3f}",ha="center",va="bottom")
    fig.tight_layout(); fig.savefig(CHARTS/filename,dpi=180); plt.close(fig)

bar(["branch_minimal","branch_local","branch_tournament"],
    ["Minimal 1-bit","LocalBP","TournamentBP"],"ipc",
    "Impact of Branch Prediction","Committed IPC","branch_ipc.png")
bar(["issue_w1","issue_w2","issue_w4"],["1-wide","2-wide","4-wide"],"ipc",
    "Multiple-Issue Performance","Committed IPC","issue_ipc.png")
bar(["smt_1thread","smt_2thread"],["1 thread","2-thread SMT"],"ipc",
    "SMT Aggregate Throughput","Aggregate committed IPC","smt_ipc.png")
bar(["low_power_performance","low_power_balanced","low_power_eco"],
    ["Performance","Balanced","Eco"],"ipc",
    "Low-Power Profiles: Performance","Committed IPC","low_power_ipc.png")
bar(["low_power_performance","low_power_balanced","low_power_eco"],
    ["Performance","Balanced","Eco"],"normalized_energy_proxy",
    "Low-Power Profiles: Normalized Energy Proxy",
    "Normalized energy proxy","low_power_energy_proxy.png")
print(CHARTS)
