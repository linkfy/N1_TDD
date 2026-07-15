"""
Add BIT Absolute.

Opcode:
    0x2C -> BIT $hhhh

Goal:
create bit_absolute(cpu), use absolute(cpu), read memory, then bit(cpu, value).

Student guidance:
Absolute operands are little-endian. `2C 02 20` targets $2002, which is the
NES PPUSTATUS register. Later, reading that address must trigger PPU side
effects in the bus/PPU layer; BIT itself only consumes the read value.
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


def test_bit_absolute_handler_exists_and_is_in_opcode_table():
    """Objective: create bit_absolute(cpu) and add 0x2C to OPCODE_TABLE."""
    assert hasattr(opcodes, "bit_absolute")
    assert callable(opcodes.bit_absolute)
    assert list(inspect.signature(opcodes.bit_absolute).parameters) == ["cpu"]
    assert opcodes.OPCODE_TABLE[0x2C] is opcodes.bit_absolute


def test_opcode_2C_bit_absolute_sets_zero_from_a_and_memory_value():
    """Objective: 2C 00 02 means BIT value at RAM[$0200]."""
    cpu, bus, rom = make_cpu_with_rom()
    rom.write(0x0000, 0x2C)
    rom.write(0x0001, 0x00)
    rom.write(0x0002, 0x02)
    bus.write(0x0200, 0b1111_0000)

    cpu.reset()
    cpu.a = 0b0000_1111
    cpu.step()

    assert (cpu.p & ZERO_FLAG) != 0
    assert cpu.a == 0b0000_1111
    assert bus.read(0x0200) == 0b1111_0000
    assert cpu.pc == 0x8003


def test_opcode_2C_bit_absolute_copies_memory_bits_7_and_6_to_n_and_v():
    """Objective: memory bits 7 and 6 are copied into Negative and Overflow."""
    cpu, bus, rom = make_cpu_with_rom()
    rom.write(0x0000, 0x2C)
    rom.write(0x0001, 0x00)
    rom.write(0x0002, 0x02)
    bus.write(0x0200, 0b1100_0000)

    cpu.reset()
    cpu.a = 0x00
    cpu.step()

    assert (cpu.p & NEGATIVE_FLAG) != 0
    assert (cpu.p & OVERFLOW_FLAG) != 0
