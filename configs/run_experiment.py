import argparse
import os
import sys
import m5
from m5.objects import (
    BranchPredictor, DerivO3CPU, LocalBP, TimingSimpleCPU, TournamentBP,
)

sys.path.insert(0, os.path.dirname(__file__))
from common import make_system

parser = argparse.ArgumentParser()
parser.add_argument("--experiment", choices=["pipeline","branch","issue","smt","low_power"], required=True)
parser.add_argument("--binary", required=True)
parser.add_argument("--binary2")
parser.add_argument("--predictor", choices=["minimal","local","tournament"], default="tournament")
parser.add_argument("--width", type=int, choices=[1,2,4], default=2)
parser.add_argument("--maxinsts", type=int, default=0)
parser.add_argument("--arg", action="append", default=[])
parser.add_argument(
    "--power-profile",
    choices=["performance", "balanced", "eco"],
    default="performance",
    help="Static DVFS and width-gating operating point for low_power runs",
)
args = parser.parse_args()

profile = {
    "performance": {"clock": "2GHz", "voltage": "1.0V", "width": 4},
    "balanced": {"clock": "1.6GHz", "voltage": "0.9V", "width": 2},
    "eco": {"clock": "1.2GHz", "voltage": "0.8V", "width": 1},
}[args.power_profile]

if args.experiment == "pipeline":
    # MinorCPU is not available in gem5's X86 build. TimingSimpleCPU provides
    # the supported in-order timing baseline for the introductory run.
    cpu = TimingSimpleCPU()
elif args.experiment == "smt":
    if not args.binary2:
        parser.error("--binary2 is required for SMT")
    cpu = DerivO3CPU(numThreads=2)
    cpu.fetchWidth = cpu.decodeWidth = cpu.renameWidth = 4
    cpu.dispatchWidth = cpu.issueWidth = cpu.wbWidth = cpu.commitWidth = 4
else:
    cpu = DerivO3CPU()
    if args.experiment in ("issue", "low_power"):
        w = profile["width"] if args.experiment == "low_power" else args.width
        cpu.fetchWidth = cpu.decodeWidth = cpu.renameWidth = w
        cpu.dispatchWidth = cpu.issueWidth = cpu.commitWidth = w
        # Keep the O3 writeback fabric at its supported default. Narrowing
        # wbWidth to one triggers a gem5 25.1 X86 timing-buffer assertion when
        # multiple memory/execution completions return in the same cycle.
    if args.predictor == "local":
        cpu.branchPred = BranchPredictor(conditionalBranchPred=LocalBP())
    elif args.predictor == "tournament":
        cpu.branchPred = BranchPredictor(
            conditionalBranchPred=TournamentBP()
        )
    else:
        # A deliberately tiny 1-bit local predictor. O3 requires a non-null
        # predictor, so this is the reproducible "prediction-minimized" baseline.
        cpu.branchPred = BranchPredictor(
            conditionalBranchPred=LocalBP(
                localPredictorSize=8, localCtrBits=1
            )
        )

if args.maxinsts:
    cpu.max_insts_any_thread = args.maxinsts

binaries = [os.path.abspath(args.binary)]
options = [args.arg]
if args.binary2:
    binaries.append(os.path.abspath(args.binary2))
    options.append([])

clock = profile["clock"] if args.experiment == "low_power" else "2GHz"
voltage = profile["voltage"] if args.experiment == "low_power" else "1.0V"
system, root = make_system(cpu, binaries, options, clock=clock, voltage=voltage)
m5.instantiate()
print("BEGIN CONFIG")
print(f"experiment={args.experiment} predictor={args.predictor} width={args.width}")
print(f"power_profile={args.power_profile} clock={clock} voltage={voltage}")
print("binaries=" + ",".join(binaries))
print("END CONFIG")
exit_event = m5.simulate()
print(f"Exiting @ tick {m5.curTick()} because {exit_event.getCause()}")
