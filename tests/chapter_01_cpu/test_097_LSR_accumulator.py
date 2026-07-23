"""
Add LSR Accumulator.

Opcode:
    0x4A -> LSR A

Goal:
map opcode 0x4A directly to lsr_a(cpu).

Student guidance:
Accumulator mode has no operand byte. Do not call an addressing helper here.
Opcode 0x4A is one byte long, so PC advances by exactly 1.
"""
import inspect

from emulator.bus.cpu_bus import CpuBus
from emulator.cpu import opcodes
from emulator.cpu.cpu import CPU
from emulator.memory.fake_rom import FakeROM
from tests.helpers import NEGATIVE_FLAG, ZERO_FLAG


CARRY_FLAG = 1 << 0


def make_cpu_with_rom():
    rom = FakeROM()
    rom.write(0x7FFC, 0x00)
    rom.write(0x7FFD, 0x80)
    bus = CpuBus(program_rom=rom)
    return CPU(bus), bus, rom


def test_lsr_accumulator_opcode_exists_and_is_in_opcode_table():
    """Objective: import lsr_a and add 0x4A to OPCODE_TABLE."""
    assert hasattr(opcodes, "lsr_a")
    assert callable(opcodes.lsr_a)
    assert list(inspect.signature(opcodes.lsr_a).parameters) == ["cpu"]
    assert opcodes.OPCODE_TABLE[0x4A] is opcodes.lsr_a


def test_opcode_4A_lsr_accumulator_shifts_a_and_advances_pc_by_one():
    """Objective: 4A means LSR A, so only A is shifted and PC advances by 1."""
    cpu, bus, rom = make_cpu_with_rom()
    rom.write(0x0000, 0x4A)

    cpu.reset()
    cpu.a = 0b0000_0110
    cpu.step()

    assert cpu.a == 0b0000_0011
    assert cpu.pc == 0x8001


def test_opcode_4A_lsr_accumulator_sets_carry_from_old_a_bit_0():
    """Objective: old A bit 0 is copied into Carry."""
    cpu, bus, rom = make_cpu_with_rom()
    rom.write(0x0000, 0x4A)

    cpu.reset()
    cpu.a = 0b0000_0011
    cpu.step()

    assert cpu.a == 0b0000_0001
    assert (cpu.p & CARRY_FLAG) != 0


def test_opcode_4A_lsr_accumulator_updates_zero_and_negative_flags():
    """Objective: A=0x01 becomes 0x00, sets Zero, and clears Negative."""
    cpu, bus, rom = make_cpu_with_rom()
    rom.write(0x0000, 0x4A)

    cpu.reset()
    cpu.p |= NEGATIVE_FLAG
    cpu.a = 0x01
    cpu.step()

    assert cpu.a == 0x00
    assert (cpu.p & ZERO_FLAG) != 0
    assert (cpu.p & NEGATIVE_FLAG) == 0
