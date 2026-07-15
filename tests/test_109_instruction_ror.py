"""
Add the ROR memory instruction behavior.

Instruction:
    ROR memory -> rotate memory[address] right through Carry

Goal:
implement ror(cpu, address) in instructions.py for memory destinations.

Student guidance:
ROR is not the same as LSR. LSR always inserts 0 into bit 7. ROR inserts the
old Carry flag into bit 7, and old bit 0 becomes the new Carry flag.
"""

from emulator.cpu.instructions import ror
from tests.helpers import NEGATIVE_FLAG, ZERO_FLAG, make_cpu


CARRY_FLAG = 1 << 0


def test_ror_memory_rotates_right_with_old_carry_clear():
    """Objective: old Carry=0 means new bit 7 becomes 0."""
    cpu = make_cpu()
    cpu.bus.write(0x0020, 0b0000_0110)

    ror(cpu, 0x0020)

    assert cpu.bus.read(0x0020) == 0b0000_0011
    assert (cpu.p & CARRY_FLAG) == 0


def test_ror_memory_rotates_right_with_old_carry_set():
    """Objective: old Carry=1 is inserted into result bit 7."""
    cpu = make_cpu()
    cpu.p |= CARRY_FLAG
    cpu.bus.write(0x0020, 0b0000_0010)

    ror(cpu, 0x0020)

    assert cpu.bus.read(0x0020) == 0b1000_0001
    assert (cpu.p & CARRY_FLAG) == 0


def test_ror_memory_sets_carry_from_old_bit_0():
    """Objective: old memory bit 0 becomes the new Carry flag."""
    cpu = make_cpu()
    cpu.bus.write(0x0020, 0b0000_0011)

    ror(cpu, 0x0020)

    assert cpu.bus.read(0x0020) == 0b0000_0001
    assert (cpu.p & CARRY_FLAG) != 0


def test_ror_memory_sets_zero_flag_when_result_is_zero():
    """Objective: 0x01 with old Carry=0 becomes 0x00 and sets Zero."""
    cpu = make_cpu()
    cpu.bus.write(0x0020, 0x01)

    ror(cpu, 0x0020)

    assert cpu.bus.read(0x0020) == 0x00
    assert (cpu.p & ZERO_FLAG) != 0
    assert (cpu.p & NEGATIVE_FLAG) == 0
    assert (cpu.p & CARRY_FLAG) != 0


def test_ror_memory_sets_negative_flag_from_result_bit_7():
    """Objective: old Carry=1 becomes result bit 7, so Negative is set."""
    cpu = make_cpu()
    cpu.p |= CARRY_FLAG
    cpu.bus.write(0x0020, 0x00)

    ror(cpu, 0x0020)

    assert cpu.bus.read(0x0020) == 0x80
    assert (cpu.p & NEGATIVE_FLAG) != 0
    assert (cpu.p & ZERO_FLAG) == 0
