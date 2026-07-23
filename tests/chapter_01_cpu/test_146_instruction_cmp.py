"""
Add the CMP instruction behavior.

Instruction:
    CMP -> compare A with value

Goal:
implement cmp(cpu, value) in instructions.py.

Student guidance:
CMP computes A - value for flags only. It does not store the subtraction result
back into A.

Flags:
    C = A >= value
    Z = A == value
    N = bit 7 of (A - value)
"""

from emulator.cpu.instructions import cmp
from tests.helpers import NEGATIVE_FLAG, ZERO_FLAG, make_cpu


CARRY_FLAG = 1 << 0
OVERFLOW_FLAG = 1 << 6


def test_cmp_sets_carry_when_a_is_greater_than_value():
    """Objective: Carry means A >= value for CMP."""
    cpu = make_cpu()
    cpu.a = 0x10

    cmp(cpu, 0x01)

    assert (cpu.p & CARRY_FLAG) != 0
    assert (cpu.p & ZERO_FLAG) == 0
    assert (cpu.p & NEGATIVE_FLAG) == 0


def test_cmp_sets_carry_and_zero_when_a_equals_value():
    """Objective: A == value sets both Carry and Zero."""
    cpu = make_cpu()
    cpu.a = 0x10

    cmp(cpu, 0x10)

    assert (cpu.p & CARRY_FLAG) != 0
    assert (cpu.p & ZERO_FLAG) != 0
    assert (cpu.p & NEGATIVE_FLAG) == 0


def test_cmp_clears_carry_and_sets_negative_when_a_is_less_than_value():
    """Objective: A < value clears Carry; wrapped subtraction can set Negative."""
    cpu = make_cpu()
    cpu.a = 0x01

    cmp(cpu, 0x02)

    assert (cpu.p & CARRY_FLAG) == 0
    assert (cpu.p & ZERO_FLAG) == 0
    assert (cpu.p & NEGATIVE_FLAG) != 0


def test_cmp_does_not_modify_accumulator_or_overflow_flag():
    """Objective: CMP only updates C/Z/N; A and Overflow are preserved."""
    cpu = make_cpu()
    cpu.a = 0x10
    cpu.p |= OVERFLOW_FLAG

    cmp(cpu, 0x01)

    assert cpu.a == 0x10
    assert (cpu.p & OVERFLOW_FLAG) != 0
