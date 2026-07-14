"""In this test we should implement the usage of rom cartridges
CPU_Bus should have 2 contructor parameters:
    program_rom: MemoryDevice | None
    ram: RAM
"""

from emulator.bus.cpu_bus import CpuBus
from emulator.memory.fake_rom import FakeROM
from emulator.memory.memory_device import MemoryDevice



def test_cpu_bus_contains_program_rom_parameter():
    rom = FakeROM()
    cpu_bus = CpuBus(program_rom=rom)

    assert hasattr(cpu_bus, "program_rom")
    assert isinstance(cpu_bus.program_rom, MemoryDevice)


def test_cpu_bus_reads_program_rom():
    """At this point 
    CPU addresses 0x8000-0xFFFF should map to
    ROM offsets 0x0000-0x7FFF (Total = 0x8000)

    https://en.wikibooks.org/wiki/NES_Programming/Memory_Map
    """

    rom = FakeROM()

    for offset in range(0x8000):
        rom.write(offset, offset & 0xFF)

    bus = CpuBus(program_rom=rom)

    for offset in range(0x8000):
        cpu_addr = 0x8000 + offset

        assert bus.read(cpu_addr) == (offset & 0xFF)

