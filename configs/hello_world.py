import argparse
import os
import m5
from m5.objects import TimingSimpleCPU
from common import make_system

parser=argparse.ArgumentParser()
parser.add_argument("--binary", required=True)
args=parser.parse_args()
cpu=TimingSimpleCPU()
system,root=make_system(cpu,[os.path.abspath(args.binary)])
m5.instantiate()
event=m5.simulate()
print(f"Exiting @ tick {m5.curTick()} because {event.getCause()}")
