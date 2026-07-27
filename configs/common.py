"""Shared classic-memory helpers for gem5 v25.1.0.1."""
from m5.objects import (
    AddrRange, Cache, DDR3_1600_8x8, MemCtrl, Process, Root, SrcClockDomain,
    System, SystemXBar, L2XBar, VoltageDomain,
)

class L1ICache(Cache):
    size = "32KiB"; assoc = 2
    tag_latency = data_latency = response_latency = 2
    mshrs = 4; tgts_per_mshr = 20

class L1DCache(Cache):
    size = "32KiB"; assoc = 2
    tag_latency = data_latency = response_latency = 2
    mshrs = 4; tgts_per_mshr = 20

class L2Cache(Cache):
    size = "256KiB"; assoc = 8
    tag_latency = data_latency = 12
    response_latency = 12; mshrs = 16; tgts_per_mshr = 12

def make_system(cpu, binaries, options=None, clock="2GHz", voltage="1.0V"):
    system = System()
    system.clk_domain = SrcClockDomain(
        clock=clock, voltage_domain=VoltageDomain(voltage=voltage)
    )
    system.mem_mode = "timing"
    system.mem_ranges = [AddrRange("512MiB")]
    # Required by gem5 when one CPU object exposes multiple thread contexts
    # (the two-workload SMT experiment).
    system.multi_thread = len(binaries) > 1
    system.cpu = cpu
    system.membus = SystemXBar()
    system.l2bus = L2XBar()
    system.l2cache = L2Cache()
    system.l2cache.cpu_side = system.l2bus.mem_side_ports
    system.l2cache.mem_side = system.membus.cpu_side_ports

    cpu.icache = L1ICache()
    cpu.dcache = L1DCache()
    cpu.icache.cpu_side = cpu.icache_port
    cpu.dcache.cpu_side = cpu.dcache_port
    cpu.icache.mem_side = system.l2bus.cpu_side_ports
    cpu.dcache.mem_side = system.l2bus.cpu_side_ports
    cpu.createInterruptController()
    for controller in cpu.interrupts:
        controller.pio = system.membus.mem_side_ports
        controller.int_requestor = system.membus.cpu_side_ports
        controller.int_responder = system.membus.mem_side_ports

    system.system_port = system.membus.cpu_side_ports
    system.mem_ctrl = MemCtrl()
    system.mem_ctrl.dram = DDR3_1600_8x8()
    system.mem_ctrl.dram.range = system.mem_ranges[0]
    system.mem_ctrl.port = system.membus.mem_side_ports

    procs = []
    options = options or [[] for _ in binaries]
    for idx, binary in enumerate(binaries):
        proc = Process(pid=100 + idx)
        proc.executable = binary
        proc.cmd = [binary] + options[idx]
        procs.append(proc)
    cpu.workload = procs if len(procs) > 1 else procs[0]
    cpu.createThreads()
    system.workload = __import__("m5.objects", fromlist=["SEWorkload"]).SEWorkload.init_compatible(binaries[0])
    return system, Root(full_system=False, system=system)
