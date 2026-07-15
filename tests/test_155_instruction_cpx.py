"""
Add the CPX instruction behavior.

Instruction:
    CPX -> compare X with value

Goal:
implement cpx(cpu, value) in instructions.py.

Student guidance:
CPX computes X - value for flags only. It does not store the subtraction result
back into X.

Flags:
    C = X >= value
    Z = X == value
    N = bit 7 of (X - value)
"""

from emulator.cpu.instructions import cpx
from tests.helpers import NEGATIVE_FLAG, ZERO_FLAG, make_cpu


CARRY_FLAG = 1 << 0
OVERFLOW_FLAG = 1 << 6


def test_cpx_sets_carry_when_x_is_greater_than_value():
    """Objective: Carry means X >= value for CPX."""
    cpu = make_cpu()
    cpu.x = 0x10

    cpx(cpu, 0x01)

    assert (cpu.p & CARRY_FLAG) != 0
    assert (cpu.p & ZERO_FLAG) == 0
    assert (cpu.p & NEGATIVE_FLAG) == 0


def test_cpx_sets_carry_and_zero_when_x_equals_value():
    """Objective: X == value sets both Carry and Zero."""
    cpu = make_cpu()
    cpu.x = 0x10

    cpx(cpu, 0x10)

    assert (cpu.p & CARRY_FLAG) != 0
    assert (cpu.p & ZERO_FLAG) != 0
    assert (cpu.p & NEGATIVE_FLAG) == 0


def test_cpx_clears_carry_and_sets_negative_when_x_is_less_than_value():
    """Objective: X < value clears Carry; wrapped subtraction can set Negative."""
    cpu = make_cpu()
    cpu.x = 0x01

    cpx(cpu, 0x02)

    assert (cpu.p & CARRY_FLAG) == 0
    assert (cpu.p & ZERO_FLAG) == 0
    assert (cpu.p & NEGATIVE_FLAG) != 0


def test_cpx_does_not_modify_x_or_overflow_flag():
    """Objective: CPX only updates C/Z/N; X and Overflow are preserved."""
    cpu = make_cpu()
    cpu.x = 0x10
    cpu.p |= OVERFLOW_FLAG

    cpx(cpu, 0x01)

    assert cpu.x == 0x10
    assert (cpu.p & OVERFLOW_FLAG) != 0
