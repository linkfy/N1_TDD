"""
Add the CPY instruction behavior.

Instruction:
    CPY -> compare Y with value

Goal:
implement cpy(cpu, value) in instructions.py.

Student guidance:
CPY computes Y - value for flags only. It does not store the subtraction result
back into Y.

Flags:
    C = Y >= value
    Z = Y == value
    N = bit 7 of (Y - value)
"""

from emulator.cpu.instructions import cpy
from tests.helpers import NEGATIVE_FLAG, ZERO_FLAG, make_cpu


CARRY_FLAG = 1 << 0
OVERFLOW_FLAG = 1 << 6


def test_cpy_sets_carry_when_y_is_greater_than_value():
    """Objective: Carry means Y >= value for CPY."""
    cpu = make_cpu()
    cpu.y = 0x10

    cpy(cpu, 0x01)

    assert (cpu.p & CARRY_FLAG) != 0
    assert (cpu.p & ZERO_FLAG) == 0
    assert (cpu.p & NEGATIVE_FLAG) == 0


def test_cpy_sets_carry_and_zero_when_y_equals_value():
    """Objective: Y == value sets both Carry and Zero."""
    cpu = make_cpu()
    cpu.y = 0x10

    cpy(cpu, 0x10)

    assert (cpu.p & CARRY_FLAG) != 0
    assert (cpu.p & ZERO_FLAG) != 0
    assert (cpu.p & NEGATIVE_FLAG) == 0


def test_cpy_clears_carry_and_sets_negative_when_y_is_less_than_value():
    """Objective: Y < value clears Carry; wrapped subtraction can set Negative."""
    cpu = make_cpu()
    cpu.y = 0x01

    cpy(cpu, 0x02)

    assert (cpu.p & CARRY_FLAG) == 0
    assert (cpu.p & ZERO_FLAG) == 0
    assert (cpu.p & NEGATIVE_FLAG) != 0


def test_cpy_does_not_modify_y_or_overflow_flag():
    """Objective: CPY only updates C/Z/N; Y and Overflow are preserved."""
    cpu = make_cpu()
    cpu.y = 0x10
    cpu.p |= OVERFLOW_FLAG

    cpy(cpu, 0x01)

    assert cpu.y == 0x10
    assert (cpu.p & OVERFLOW_FLAG) != 0
