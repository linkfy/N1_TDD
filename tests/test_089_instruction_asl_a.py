"""
Add the ASL accumulator instruction behavior.

Instruction:
    ASL A -> A = A << 1

Goal:
implement asl_a(cpu) in instructions.py for the accumulator destination.

Why this is separate from asl(cpu, address):
ASL A does not decode an address and does not touch memory. The destination is
the accumulator register itself, so the instruction must read and write cpu.a.
"""

from emulator.cpu.instructions import asl_a
from tests.helpers import NEGATIVE_FLAG, ZERO_FLAG, make_cpu


CARRY_FLAG = 1 << 0


def test_asl_a_shifts_accumulator_left():
    """Objective: A value 0b0000_0011 becomes 0b0000_0110."""
    cpu = make_cpu()
    cpu.a = 0b0000_0011

    asl_a(cpu)

    assert cpu.a == 0b0000_0110


def test_asl_a_sets_carry_from_old_accumulator_bit_7():
    """Objective: old A bit 7 is moved into Carry before the 8-bit wrap."""
    cpu = make_cpu()
    cpu.a = 0b1000_0001

    asl_a(cpu)

    assert cpu.a == 0b0000_0010
    assert (cpu.p & CARRY_FLAG) != 0


def test_asl_a_clears_carry_when_old_accumulator_bit_7_was_clear():
    """Objective: Carry is cleared when original A did not have bit 7 set."""
    cpu = make_cpu()
    cpu.p |= CARRY_FLAG
    cpu.a = 0b0100_0000

    asl_a(cpu)

    assert cpu.a == 0b1000_0000
    assert (cpu.p & CARRY_FLAG) == 0


def test_asl_a_sets_zero_flag_when_result_is_zero():
    """Objective: A=0x80 shifts to 0x00 and sets Zero flag."""
    cpu = make_cpu()
    cpu.a = 0x80

    asl_a(cpu)

    assert cpu.a == 0x00
    assert (cpu.p & ZERO_FLAG) != 0
    assert (cpu.p & NEGATIVE_FLAG) == 0


def test_asl_a_sets_negative_flag_from_result_bit_7():
    """Objective: A=0x40 shifts to 0x80, so Negative flag is set."""
    cpu = make_cpu()
    cpu.a = 0x40

    asl_a(cpu)

    assert cpu.a == 0x80
    assert (cpu.p & NEGATIVE_FLAG) != 0
    assert (cpu.p & ZERO_FLAG) == 0


def test_asl_a_does_not_write_shifted_result_to_memory():
    """Objective: ASL A writes to A only; it must not treat A as a memory address."""
    cpu = make_cpu()
    cpu.a = 0x20
    cpu.bus.write(0x0020, 0x99)

    asl_a(cpu)

    assert cpu.a == 0x40
    assert cpu.bus.read(0x0020) == 0x99
