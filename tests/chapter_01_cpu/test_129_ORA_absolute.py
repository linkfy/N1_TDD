"""
Add ORA Absolute.

Opcode:
    0x0D -> ORA $hhhh

Goal:
create ora_absolute(cpu), use absolute(cpu), read memory, then or_a(cpu, value).

Student guidance:
Absolute operands are little-endian. `0D 00 02` targets $0200.
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


def test_ora_absolute_handler_exists_and_is_in_opcode_table():
    """Objective: create ora_absolute(cpu) and add 0x0D to OPCODE_TABLE."""
    assert hasattr(opcodes, "ora_absolute")
    assert callable(opcodes.ora_absolute)
    assert list(inspect.signature(opcodes.ora_absolute).parameters) == ["cpu"]
    assert opcodes.OPCODE_TABLE[0x0D] is opcodes.ora_absolute


def test_opcode_0D_ora_absolute_reads_memory_value():
    """Objective: 0D 00 02 means ORA value at RAM[$0200]."""
    cpu, bus, rom = make_cpu_with_rom()
    rom.write(0x0000, 0x0D)
    rom.write(0x0001, 0x00)
    rom.write(0x0002, 0x02)
    bus.write(0x0200, 0x0F)

    cpu.reset()
    cpu.a = 0xF0
    cpu.step()

    assert cpu.a == 0xFF
    assert cpu.pc == 0x8003
