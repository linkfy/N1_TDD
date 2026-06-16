"""In this test we should implement the usage of CPU reset method
"""

from emulator.bus.cpu_bus import CpuBus
from emulator.cpu.cpu import CPU
from emulator.memory.fake_rom import FakeROM



def test_cpu_reset_initializes_state():
    """
    For simplicity, this emulator models a power-on reset.
    According to NESdev, after power-up the stack pointer
    is initialized to 0xFD.

    https://www.nesdev.org/wiki/CPU_power_up_state
    - cpu.pc = ($FFFC) [Read internal ROM value]
    - cpu.s = 0xFD 
    - cpu.p = 0x04 
    """

    rom = FakeROM()

    rom.write(0x7FFC, 0x00)
    rom.write(0x7FFD, 0x80)

    bus = CpuBus(program_rom=rom)

    cpu = CPU(bus)
    

    cpu.reset()

    assert cpu.pc == 0x8000
    assert cpu.s == 0xFD
    assert cpu.p == 0x04

