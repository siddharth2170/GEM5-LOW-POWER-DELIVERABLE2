#!/usr/bin/env python3
import csv
from html import escape
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
RESULTS=ROOT/"results"
rows={r["run"]:r for r in csv.DictReader((RESULTS/"summary.csv").open())}
CHARTS=RESULTS/"charts"; CHARTS.mkdir(exist_ok=True)

def value(run,key):
    raw=rows.get(run,{}).get(key,"")
    return float(raw) if raw not in ("",None,"None") else 0.0

def bar(names, labels, key, title, ylabel, filename):
    vals=[value(n,key) for n in names]
    width, height = 960, 576
    left, right, top, bottom = 100, 40, 70, 100
    plot_w, plot_h = width-left-right, height-top-bottom
    ceiling = max(vals) * 1.18 if max(vals, default=0) > 0 else 1
    colors = ["#4472C4","#70AD47","#ED7D31","#A5A5A5"]
    slot = plot_w / max(len(vals), 1)
    bar_w = slot * .55
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="white"/>',
        f'<text x="{width/2}" y="35" text-anchor="middle" font-family="Arial" font-size="25" font-weight="bold">{escape(title)}</text>',
        f'<line x1="{left}" y1="{top}" x2="{left}" y2="{top+plot_h}" stroke="#444"/>',
        f'<line x1="{left}" y1="{top+plot_h}" x2="{left+plot_w}" y2="{top+plot_h}" stroke="#444"/>',
        f'<text x="24" y="{top+plot_h/2}" transform="rotate(-90 24 {top+plot_h/2})" text-anchor="middle" font-family="Arial" font-size="17">{escape(ylabel)}</text>',
    ]
    for tick in range(5):
        val = ceiling * tick / 4
        y = top + plot_h - (val/ceiling)*plot_h
        parts += [
            f'<line x1="{left}" y1="{y:.1f}" x2="{left+plot_w}" y2="{y:.1f}" stroke="#dddddd"/>',
            f'<text x="{left-12}" y="{y+5:.1f}" text-anchor="end" font-family="Arial" font-size="14">{val:.2f}</text>',
        ]
    for i,(label,val) in enumerate(zip(labels,vals)):
        x = left + i*slot + (slot-bar_w)/2
        h = (val/ceiling)*plot_h
        y = top + plot_h - h
        parts += [
            f'<rect x="{x:.1f}" y="{y:.1f}" width="{bar_w:.1f}" height="{h:.1f}" fill="{colors[i%len(colors)]}"/>',
            f'<text x="{x+bar_w/2:.1f}" y="{y-8:.1f}" text-anchor="middle" font-family="Arial" font-size="16">{val:.3f}</text>',
            f'<text x="{x+bar_w/2:.1f}" y="{top+plot_h+30}" text-anchor="middle" font-family="Arial" font-size="16">{escape(label)}</text>',
        ]
    parts.append("</svg>")
    (CHARTS/filename).write_text("\n".join(parts))

bar(["branch_minimal","branch_local","branch_tournament"],
    ["Minimal 1-bit","LocalBP","TournamentBP"],"ipc",
    "Impact of Branch Prediction","Committed IPC","branch_ipc.svg")
bar(["issue_w1","issue_w2","issue_w4"],["1-wide","2-wide","4-wide"],"ipc",
    "Multiple-Issue Performance","Committed IPC","issue_ipc.svg")
bar(["smt_1thread","smt_2thread"],["1 thread","2-thread SMT"],"ipc",
    "SMT Aggregate Throughput","Aggregate committed IPC","smt_ipc.svg")
bar(["low_power_performance","low_power_balanced","low_power_eco"],
    ["Performance","Balanced","Eco"],"ipc",
    "Low-Power Profiles: Performance","Committed IPC","low_power_ipc.svg")
bar(["low_power_performance","low_power_balanced","low_power_eco"],
    ["Performance","Balanced","Eco"],"normalized_energy_proxy",
    "Low-Power Profiles: Normalized Energy Proxy",
    "Normalized energy proxy","low_power_energy_proxy.svg")
print(CHARTS)
