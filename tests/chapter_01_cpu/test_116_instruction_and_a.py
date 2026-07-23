"""
Add the AND instruction behavior.

Instruction:
    AND -> A = A & value

Goal:
implement and_a(cpu, value) in instructions.py.

Student guidance:
AND always stores the result in A. The operand can come from immediate mode or
from memory, so this instruction function receives a value, not an address.
"""

from emulator.cpu.instructions import and_a
from tests.helpers import NEGATIVE_FLAG, ZERO_FLAG, make_cpu


CARRY_FLAG = 1 << 0
OVERFLOW_FLAG = 1 << 6


def test_and_a_stores_bitwise_and_result_in_accumulator():
    """Objective: A becomes A & value."""
    cpu = make_cpu()
    cpu.a = 0b1100_1010

    and_a(cpu, 0b1010_1100)

    assert cpu.a == 0b1000_1000


def test_and_a_sets_zero_flag_when_result_is_zero():
    """Objective: when A & value is 0, Zero flag is set."""
    cpu = make_cpu()
    cpu.a = 0b0000_1111


    and_a(cpu, 0b1111_0000)


    assert cpu.a == 0x00
    assert (cpu.p & ZERO_FLAG) != 0
    assert (cpu.p & NEGATIVE_FLAG) == 0


def test_and_a_sets_negative_flag_from_result_bit_7():
    """Objective: if result bit 7 is set, Negative flag is set."""
    cpu = make_cpu()
    cpu.a = 0b1000_1111

    and_a(cpu, 0b1111_0000)

    assert cpu.a == 0b1000_0000
    assert (cpu.p & NEGATIVE_FLAG) != 0
    assert (cpu.p & ZERO_FLAG) == 0


def test_and_a_does_not_modify_carry_or_overflow_flags():
    """Objective: AND only updates Z/N; Carry and Overflow are preserved."""
    cpu = make_cpu()
    cpu.a = 0xFF
    cpu.p |= CARRY_FLAG
    cpu.p |= OVERFLOW_FLAG

    and_a(cpu, 0x0F)

    assert cpu.a == 0x0F
    assert (cpu.p & CARRY_FLAG) != 0
    assert (cpu.p & OVERFLOW_FLAG) != 0
