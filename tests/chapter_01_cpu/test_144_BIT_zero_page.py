"""
Add BIT Zero Page.

Opcode:
    0x24 -> BIT $nn

Goal:
create bit_zero_page(cpu), use zero_page(cpu), read memory, then bit(cpu, value).

Student guidance:
The operand byte is the zero-page address where the tested value lives.
BIT does not modify A or memory; it only updates Z, N, and V.
"""
import inspect

from emulator.bus.cpu_bus import CpuBus
from emulator.cpu import opcodes
from emulator.cpu.cpu import CPU
from emulator.memory.fake_rom import FakeROM
from tests.helpers import NEGATIVE_FLAG, ZERO_FLAG


OVERFLOW_FLAG = 1 << 6


def make_cpu_with_rom():
    rom = FakeROM()
    rom.write(0x7FFC, 0x00)
    rom.write(0x7FFD, 0x80)
    bus = CpuBus(program_rom=rom)
    return CPU(bus), bus, rom


def test_bit_zero_page_handler_exists_and_is_in_opcode_table():
    """Objective: create bit_zero_page(cpu) and add 0x24 to OPCODE_TABLE."""
    assert hasattr(opcodes, "bit_zero_page")
    assert callable(opcodes.bit_zero_page)
    assert list(inspect.signature(opcodes.bit_zero_page).parameters) == ["cpu"]
    assert opcodes.OPCODE_TABLE[0x24] is opcodes.bit_zero_page


def test_opcode_24_bit_zero_page_sets_zero_from_a_and_memory_value():
    """Objective: 24 10 means BIT value at RAM[$0010]."""
    cpu, bus, rom = make_cpu_with_rom()
    rom.write(0x0000, 0x24)
    rom.write(0x0001, 0x10)
    bus.write(0x0010, 0b1111_0000)

    cpu.reset()
    cpu.a = 0b0000_1111
    cpu.step()

    assert (cpu.p & ZERO_FLAG) != 0
    assert cpu.a == 0b0000_1111
    assert bus.read(0x0010) == 0b1111_0000
    assert cpu.pc == 0x8002


def test_opcode_24_bit_zero_page_copies_memory_bits_7_and_6_to_n_and_v():
    """Objective: memory bits 7 and 6 are copied into Negative and Overflow."""
    cpu, bus, rom = make_cpu_with_rom()
    rom.write(0x0000, 0x24)
    rom.write(0x0001, 0x10)
    bus.write(0x0010, 0b1100_0000)

    cpu.reset()
    cpu.a = 0x00
    cpu.step()

    assert (cpu.p & NEGATIVE_FLAG) != 0
    assert (cpu.p & OVERFLOW_FLAG) != 0
