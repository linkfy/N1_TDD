"""
Add the DEY instruction behavior.

Instruction:
    DEY -> Y = Y - 1

Goal:
implement dey(cpu) in instructions.py.

Important:
DEY only modifies the Y register, Zero flag, and Negative flag.
It must not modify Carry or Overflow.
"""

from emulator.cpu.instructions import dey
from tests.helpers import NEGATIVE_FLAG, ZERO_FLAG, make_cpu


CARRY_FLAG = 1 << 0
OVERFLOW_FLAG = 1 << 6


def test_dey_decrements_y_register():
    """Objective: Y decreases by one and remains an 8-bit register value."""
    cpu = make_cpu()
    cpu.y = 0x10

    dey(cpu)

    assert cpu.y == 0x0F


def test_dey_wraps_from_00_to_ff_and_sets_negative_flag():
    """Objective: 0x00 - 1 wraps to 0xFF and sets Negative flag."""
    cpu = make_cpu()
    cpu.y = 0x00

    dey(cpu)

    assert cpu.y == 0xFF
    assert (cpu.p & NEGATIVE_FLAG) != 0
    assert (cpu.p & ZERO_FLAG) == 0


def test_dey_sets_zero_flag_when_result_is_zero():
    """Objective: 0x01 - 1 becomes 0x00 and sets Zero flag."""
    cpu = make_cpu()
    cpu.y = 0x01

    dey(cpu)

    assert cpu.y == 0x00
    assert (cpu.p & ZERO_FLAG) != 0
    assert (cpu.p & NEGATIVE_FLAG) == 0


def test_dey_does_not_modify_carry_or_overflow_flags():
    """Objective: DEY updates Z/N only; Carry and Overflow are preserved."""
    cpu = make_cpu()
    cpu.y = 0x10
    cpu.p |= CARRY_FLAG
    cpu.p |= OVERFLOW_FLAG

    dey(cpu)

    assert cpu.y == 0x0F
    assert (cpu.p & CARRY_FLAG) != 0
    assert (cpu.p & OVERFLOW_FLAG) != 0
