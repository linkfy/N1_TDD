"""
Add the INY instruction behavior.

Instruction:
    INY -> Y = Y + 1

Goal:
implement iny(cpu) in instructions.py.

Important:
INY only modifies the Y register, Zero flag, and Negative flag.
It must not modify Carry or Overflow.
"""

from emulator.cpu.instructions import iny
from tests.helpers import NEGATIVE_FLAG, ZERO_FLAG, make_cpu


CARRY_FLAG = 1 << 0
OVERFLOW_FLAG = 1 << 6


def test_iny_increments_y_register():
    """Objective: Y increases by one and remains an 8-bit register value."""
    cpu = make_cpu()
    cpu.y = 0x10

    iny(cpu)

    assert cpu.y == 0x11


def test_iny_wraps_from_ff_to_00_and_sets_zero_flag():
    """Objective: 0xFF + 1 wraps to 0x00 and sets Zero flag."""
    cpu = make_cpu()
    cpu.y = 0xFF

    iny(cpu)

    assert cpu.y == 0x00
    assert (cpu.p & ZERO_FLAG) != 0
    assert (cpu.p & NEGATIVE_FLAG) == 0


def test_iny_sets_negative_flag_when_result_has_bit_7_set():
    """Objective: 0x7F + 1 becomes 0x80, so Negative flag is set."""
    cpu = make_cpu()
    cpu.y = 0x7F

    iny(cpu)

    assert cpu.y == 0x80
    assert (cpu.p & NEGATIVE_FLAG) != 0
    assert (cpu.p & ZERO_FLAG) == 0


def test_iny_does_not_modify_carry_or_overflow_flags():
    """Objective: INY updates Z/N only; Carry and Overflow are preserved."""
    cpu = make_cpu()
    cpu.y = 0x01
    cpu.p |= CARRY_FLAG
    cpu.p |= OVERFLOW_FLAG

    iny(cpu)

    assert cpu.y == 0x02
    assert (cpu.p & CARRY_FLAG) != 0
    assert (cpu.p & OVERFLOW_FLAG) != 0
