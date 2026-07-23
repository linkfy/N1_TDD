"""
Add AND Absolute.

Opcode:
    0x2D -> AND $hhhh

Goal:
create and_absolute(cpu), use absolute(cpu), read memory, then and_a(cpu, value).

Student guidance:
Absolute operands are little-endian. `2D 00 02` targets $0200.
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


def test_and_absolute_handler_exists_and_is_in_opcode_table():
    """Objective: create and_absolute(cpu) and add 0x2D to OPCODE_TABLE."""
    assert hasattr(opcodes, "and_absolute")
    assert callable(opcodes.and_absolute)
    assert list(inspect.signature(opcodes.and_absolute).parameters) == ["cpu"]
    assert opcodes.OPCODE_TABLE[0x2D] is opcodes.and_absolute


def test_opcode_2D_and_absolute_reads_memory_value():
    """Objective: 2D 00 02 means AND value at RAM[$0200]."""
    cpu, bus, rom = make_cpu_with_rom()
    rom.write(0x0000, 0x2D)
    rom.write(0x0001, 0x00)
    rom.write(0x0002, 0x02)
    bus.write(0x0200, 0x0F)

    cpu.reset()
    cpu.a = 0xF3
    cpu.step()

    assert cpu.a == 0x03
    assert cpu.pc == 0x8003
