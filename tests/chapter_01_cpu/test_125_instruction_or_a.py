"""
Add the ORA instruction behavior.

Instruction:
    ORA -> A = A | value

Goal:
implement or_a(cpu, value) in instructions.py.

Student guidance:
6502 calls bitwise OR `ORA`. It always stores the result in A. The operand can
come from immediate mode or memory, so this function receives a value.
"""

from emulator.cpu.instructions import or_a
from tests.helpers import NEGATIVE_FLAG, ZERO_FLAG, make_cpu


CARRY_FLAG = 1 << 0
OVERFLOW_FLAG = 1 << 6


def test_or_a_stores_bitwise_or_result_in_accumulator():
    """Objective: A becomes A | value."""
    cpu = make_cpu()
    cpu.a = 0b1100_0000

    or_a(cpu, 0b0000_1010)

    assert cpu.a == 0b1100_1010


def test_or_a_sets_zero_flag_when_result_is_zero():
    """Objective: when A | value is 0, Zero flag is set."""
    cpu = make_cpu()
    cpu.a = 0x00

    or_a(cpu, 0x00)

    assert cpu.a == 0x00
    assert (cpu.p & ZERO_FLAG) != 0
    assert (cpu.p & NEGATIVE_FLAG) == 0


def test_or_a_sets_negative_flag_from_result_bit_7():
    """Objective: if result bit 7 is set, Negative flag is set."""
    cpu = make_cpu()
    cpu.a = 0x01

    or_a(cpu, 0x80)

    assert cpu.a == 0x81
    assert (cpu.p & NEGATIVE_FLAG) != 0
    assert (cpu.p & ZERO_FLAG) == 0


def test_or_a_does_not_modify_carry_or_overflow_flags():
    """Objective: ORA only updates Z/N; Carry and Overflow are preserved."""
    cpu = make_cpu()
    cpu.a = 0x00
    cpu.p |= CARRY_FLAG
    cpu.p |= OVERFLOW_FLAG

    or_a(cpu, 0x0F)

    assert cpu.a == 0x0F
    assert (cpu.p & CARRY_FLAG) != 0
    assert (cpu.p & OVERFLOW_FLAG) != 0
