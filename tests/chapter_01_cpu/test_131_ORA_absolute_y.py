"""
Add ORA Absolute,Y.

Opcode:
    0x19 -> ORA $hhhh,Y

Goal:
create ora_absolute_y(cpu), use absolute_y(cpu), read memory, then or_a(cpu, value).

Student guidance:
Decode the 16-bit base address first, then add Y.
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


def test_ora_absolute_y_handler_exists_and_is_in_opcode_table():
    """Objective: create ora_absolute_y(cpu) and add 0x19 to OPCODE_TABLE."""
    assert hasattr(opcodes, "ora_absolute_y")
    assert callable(opcodes.ora_absolute_y)
    assert list(inspect.signature(opcodes.ora_absolute_y).parameters) == ["cpu"]
    assert opcodes.OPCODE_TABLE[0x19] is opcodes.ora_absolute_y


def test_opcode_19_ora_absolute_y_reads_indexed_memory_value():
    """Objective: 19 00 02 with Y=0x04 reads RAM[$0204]."""
    cpu, bus, rom = make_cpu_with_rom()
    rom.write(0x0000, 0x19)
    rom.write(0x0001, 0x00)
    rom.write(0x0002, 0x02)
    bus.write(0x0204, 0x0F)

    cpu.reset()
    cpu.y = 0x04
    cpu.a = 0xF0
    cpu.step()

    assert cpu.a == 0xFF
    assert cpu.pc == 0x8003
