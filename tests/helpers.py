from emulator.bus.cpu_bus import CpuBus
from emulator.cpu.cpu import CPU
from emulator.memory.fake_rom import FakeROM

# Methods used on test12 and beyond
def make_cpu():
    return CPU(CpuBus())

def make_rom():
    rom = FakeROM()

    # Reset Vector
    rom.write(0x7FFC, 0x00)
    rom.write(0x7FFD, 0x80)

    return rom


