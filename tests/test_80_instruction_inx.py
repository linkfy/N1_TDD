"""
Add the INX instruction behavior.

Instruction:
    INX -> X = X + 1

Goal:
implement inx(cpu) in instructions.py.

Important:
INX only modifies the X register, Zero flag, and Negative flag.
It must not modify Carry or Overflow.
"""

from emulator.cpu.instructions import inx
from tests.helpers import NEGATIVE_FLAG, ZERO_FLAG, make_cpu


CARRY_FLAG = 1 << 0
OVERFLOW_FLAG = 1 << 6


def test_inx_increments_x_register():
    """Objective: X increases by one and remains an 8-bit register value."""
    cpu = make_cpu()
    cpu.x = 0x10

    inx(cpu)

    assert cpu.x == 0x11


def test_inx_wraps_from_ff_to_00_and_sets_zero_flag():
    """Objective: 0xFF + 1 wraps to 0x00 and sets Zero flag."""
    cpu = make_cpu()
    cpu.x = 0xFF

    inx(cpu)

    assert cpu.x == 0x00
    assert (cpu.p & ZERO_FLAG) != 0
    assert (cpu.p & NEGATIVE_FLAG) == 0


def test_inx_sets_negative_flag_when_result_has_bit_7_set():
    """Objective: 0x7F + 1 becomes 0x80, so Negative flag is set."""
    cpu = make_cpu()
    cpu.x = 0x7F

    inx(cpu)

    assert cpu.x == 0x80
    assert (cpu.p & NEGATIVE_FLAG) != 0
    assert (cpu.p & ZERO_FLAG) == 0


def test_inx_does_not_modify_carry_or_overflow_flags():
    """Objective: INX updates Z/N only; Carry and Overflow are preserved."""
    cpu = make_cpu()
    cpu.x = 0x01
    cpu.p |= CARRY_FLAG
    cpu.p |= OVERFLOW_FLAG

    inx(cpu)

    assert cpu.x == 0x02
    assert (cpu.p & CARRY_FLAG) != 0
    assert (cpu.p & OVERFLOW_FLAG) != 0
