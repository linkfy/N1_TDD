"""
Add the BIT instruction behavior.

Instruction:
    BIT -> test bits in value using A

Goal:
implement bit(cpu, value) in instructions.py.

Student guidance:
BIT is a test-only instruction. It does not store A & value back into A.
It only updates flags:
    Z = (A & value) == 0
    N = value bit 7
    V = value bit 6
"""

from emulator.cpu.instructions import bit
from tests.helpers import NEGATIVE_FLAG, ZERO_FLAG, make_cpu


CARRY_FLAG = 1 << 0
OVERFLOW_FLAG = 1 << 6


def test_bit_sets_zero_flag_when_a_and_value_is_zero():
    """Objective: if A & value is 0, Zero flag is set."""
    cpu = make_cpu()
    cpu.a = 0b0000_1111

    bit(cpu, 0b1111_0000)

    assert (cpu.p & ZERO_FLAG) != 0


def test_bit_clears_zero_flag_when_a_and_value_is_not_zero():
    """Objective: if A & value is nonzero, Zero flag is cleared."""
    cpu = make_cpu()
    cpu.p |= ZERO_FLAG
    cpu.a = 0b0000_1111

    bit(cpu, 0b0000_0001)

    assert (cpu.p & ZERO_FLAG) == 0


def test_bit_sets_negative_flag_from_value_bit_7():
    """Objective: BIT copies value bit 7 into Negative flag."""
    cpu = make_cpu()
    cpu.a = 0x00

    bit(cpu, 0b1000_0000)

    assert (cpu.p & NEGATIVE_FLAG) != 0


def test_bit_sets_overflow_flag_from_value_bit_6():
    """Objective: BIT copies value bit 6 into Overflow flag."""
    cpu = make_cpu()
    cpu.a = 0x00

    bit(cpu, 0b0100_0000)

    assert (cpu.p & OVERFLOW_FLAG) != 0


def test_bit_clears_negative_and_overflow_when_value_bits_are_clear():
    """Objective: N and V follow value bits 7 and 6, including clearing them."""
    cpu = make_cpu()
    cpu.p |= NEGATIVE_FLAG
    cpu.p |= OVERFLOW_FLAG
    cpu.a = 0xFF

    bit(cpu, 0b0011_1111)

    assert (cpu.p & NEGATIVE_FLAG) == 0
    assert (cpu.p & OVERFLOW_FLAG) == 0


def test_bit_does_not_modify_accumulator_or_carry_flag():
    """Objective: BIT only updates Z/N/V; A and Carry are preserved."""
    cpu = make_cpu()
    cpu.a = 0b1010_1010
    cpu.p |= CARRY_FLAG

    bit(cpu, 0b1111_0000)

    assert cpu.a == 0b1010_1010
    assert (cpu.p & CARRY_FLAG) != 0
