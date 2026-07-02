from emulator.bus.cpu_bus import CpuBus
from emulator.cpu.cpu import CPU


ZERO_FLAG = 1 << 1
NEGATIVE_FLAG = 1 << 7


def make_cpu():
    return CPU(CpuBus())
