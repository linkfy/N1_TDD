"""
Add ORA Absolute,X.

Opcode:
    0x1D -> ORA $hhhh,X

Goal:
create ora_absolute_x(cpu), use absolute_x(cpu), read memory, then or_a(cpu, value).

Student guidance:
Decode the 16-bit base address first, then add X.
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


def test_ora_absolute_x_handler_exists_and_is_in_opcode_table():
    """Objective: create ora_absolute_x(cpu) and add 0x1D to OPCODE_TABLE."""
    assert hasattr(opcodes, "ora_absolute_x")
    assert callable(opcodes.ora_absolute_x)
    assert list(inspect.signature(opcodes.ora_absolute_x).parameters) == ["cpu"]
    assert opcodes.OPCODE_TABLE[0x1D] is opcodes.ora_absolute_x


def test_opcode_1D_ora_absolute_x_reads_indexed_memory_value():
    """Objective: 1D 00 02 with X=0x04 reads RAM[$0204]."""
    cpu, bus, rom = make_cpu_with_rom()
    rom.write(0x0000, 0x1D)
    rom.write(0x0001, 0x00)
    rom.write(0x0002, 0x02)
    bus.write(0x0204, 0x0F)

    cpu.reset()
    cpu.x = 0x04
    cpu.a = 0xF0
    cpu.step()

    assert cpu.a == 0xFF
    assert cpu.pc == 0x8003
