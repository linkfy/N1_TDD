"""
Add CMP Zero Page.

Opcode:
    0xC5 -> CMP $nn

Goal:
create cmp_zero_page(cpu), use zero_page(cpu), read memory, then cmp(cpu, value).

Student guidance:
The operand byte is the zero-page address where the compared value lives.
"""
import inspect

from emulator.bus.cpu_bus import CpuBus
from emulator.cpu import opcodes
from emulator.cpu.cpu import CPU
from emulator.memory.fake_rom import FakeROM


CARRY_FLAG = 1 << 0


def make_cpu_with_rom():
    rom = FakeROM()
    rom.write(0x7FFC, 0x00)
    rom.write(0x7FFD, 0x80)
    bus = CpuBus(program_rom=rom)
    return CPU(bus), bus, rom


def test_cmp_zero_page_handler_exists_and_is_in_opcode_table():
    """Objective: create cmp_zero_page(cpu) and add 0xC5 to OPCODE_TABLE."""
    assert hasattr(opcodes, "cmp_zero_page")
    assert callable(opcodes.cmp_zero_page)
    assert list(inspect.signature(opcodes.cmp_zero_page).parameters) == ["cpu"]
    assert opcodes.OPCODE_TABLE[0xC5] is opcodes.cmp_zero_page


def test_opcode_C5_cmp_zero_page_reads_memory_value_and_compares():
    """Objective: C5 10 means compare A with RAM[$0010]."""
    cpu, bus, rom = make_cpu_with_rom()
    rom.write(0x0000, 0xC5)
    rom.write(0x0001, 0x10)
    bus.write(0x0010, 0x10)

    cpu.reset()
    cpu.a = 0x20
    cpu.step()

    assert cpu.a == 0x20
    assert (cpu.p & CARRY_FLAG) != 0
    assert cpu.pc == 0x8002
