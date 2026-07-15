"""
Add ROR Absolute,X.

Opcode:
    0x7E -> ROR $hhhh,X

Goal:
create ror_absolute_x(cpu), use absolute_x(cpu), then ror(cpu, address).

Student guidance:
Absolute,X first decodes the 16-bit little-endian base address, then adds X.
For `7E 00 02` with X=0x04, the target address is $0204.
"""
import inspect

from emulator.bus.cpu_bus import CpuBus
from emulator.cpu import opcodes
from emulator.cpu.cpu import CPU
from emulator.memory.fake_rom import FakeROM


def make_cpu_with_rom():
    rom = FakeROM()
    rom.write(0x7FFC, 0x00)
    rom.write(0x7FFD, 0x80)
    bus = CpuBus(program_rom=rom)
    return CPU(bus), bus, rom


def test_ror_absolute_x_handler_exists_and_is_in_opcode_table():
    """Objective: create ror_absolute_x(cpu) and add 0x7E to OPCODE_TABLE."""
    assert hasattr(opcodes, "ror_absolute_x")
    assert callable(opcodes.ror_absolute_x)
    assert list(inspect.signature(opcodes.ror_absolute_x).parameters) == ["cpu"]
    assert opcodes.OPCODE_TABLE[0x7E] is opcodes.ror_absolute_x


def test_opcode_7E_ror_absolute_x_rotates_indexed_memory_value():
    """Objective: 7E 00 02 with X=0x04 rotates RAM[$0204]."""
    cpu, bus, rom = make_cpu_with_rom()
    rom.write(0x0000, 0x7E)
    rom.write(0x0001, 0x00)
    rom.write(0x0002, 0x02)
    bus.write(0x0204, 0b0000_0110)

    cpu.reset()
    cpu.x = 0x04
    cpu.step()

    assert bus.read(0x0204) == 0b0000_0011
    assert cpu.pc == 0x8003
