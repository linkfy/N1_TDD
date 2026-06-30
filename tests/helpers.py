from emulator.bus.cpu_bus import CpuBus
from emulator.cpu.cpu import CPU


def make_cpu():
    return CPU(CpuBus())
