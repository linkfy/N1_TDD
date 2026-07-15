"""
Add AND Zero Page.

Opcode:
    0x25 -> AND $nn

Goal:
create and_zero_page(cpu), use zero_page(cpu), read memory, then and_a(cpu, value).

Student guidance:
The operand byte is the zero-page address where the value lives.
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


def test_and_zero_page_handler_exists_and_is_in_opcode_table():
    """Objective: create and_zero_page(cpu) and add 0x25 to OPCODE_TABLE."""
    assert hasattr(opcodes, "and_zero_page")
    assert callable(opcodes.and_zero_page)
    assert list(inspect.signature(opcodes.and_zero_page).parameters) == ["cpu"]
    assert opcodes.OPCODE_TABLE[0x25] is opcodes.and_zero_page


def test_opcode_25_and_zero_page_reads_memory_value_and_updates_a():
    """Objective: 25 10 means AND value at RAM[$0010]."""
    cpu, bus, rom = make_cpu_with_rom()
    rom.write(0x0000, 0x25)
    rom.write(0x0001, 0x10)
    bus.write(0x0010, 0x0F)

    cpu.reset()
    cpu.a = 0xF3
    cpu.step()

    assert cpu.a == 0x03
    assert cpu.pc == 0x8002
