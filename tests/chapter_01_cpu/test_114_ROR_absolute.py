"""
Add ROR Absolute.

Opcode:
    0x6E -> ROR $hhhh

Goal:
create ror_absolute(cpu), use absolute(cpu), then ror(cpu, address).

Student guidance:
Absolute operands are little-endian. For `6E 00 02`, the target address is
$0200, not $0002.
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


def test_ror_absolute_handler_exists_and_is_in_opcode_table():
    """Objective: create ror_absolute(cpu) and add 0x6E to OPCODE_TABLE."""
    assert hasattr(opcodes, "ror_absolute")
    assert callable(opcodes.ror_absolute)
    assert list(inspect.signature(opcodes.ror_absolute).parameters) == ["cpu"]
    assert opcodes.OPCODE_TABLE[0x6E] is opcodes.ror_absolute


def test_opcode_6E_ror_absolute_rotates_memory_value():
    """Objective: 6E 00 02 means ROR $0200, so RAM[$0200] is rotated."""
    cpu, bus, rom = make_cpu_with_rom()
    rom.write(0x0000, 0x6E)
    rom.write(0x0001, 0x00)
    rom.write(0x0002, 0x02)
    bus.write(0x0200, 0b0000_0110)

    cpu.reset()
    cpu.step()

    assert bus.read(0x0200) == 0b0000_0011
    assert cpu.pc == 0x8003
