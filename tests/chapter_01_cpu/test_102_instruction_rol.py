"""
Add the ROL memory instruction behavior.

Instruction:
    ROL memory -> rotate memory[address] left through Carry

Goal:
implement rol(cpu, address) in instructions.py for memory destinations.

Student guidance:
ROL is not the same as ASL. ASL always inserts 0 into bit 0. ROL inserts the
old Carry flag into bit 0, and old bit 7 becomes the new Carry flag.
"""

from emulator.cpu.instructions import rol
from tests.helpers import NEGATIVE_FLAG, ZERO_FLAG, make_cpu


CARRY_FLAG = 1 << 0


def test_rol_memory_rotates_left_with_old_carry_clear():
    """Objective: old Carry=0 means new bit 0 becomes 0."""
    cpu = make_cpu()
    cpu.bus.write(0x0020, 0b0000_0011)

    rol(cpu, 0x0020)

    assert cpu.bus.read(0x0020) == 0b0000_0110
    assert (cpu.p & CARRY_FLAG) == 0


def test_rol_memory_rotates_left_with_old_carry_set():
    """Objective: old Carry=1 is inserted into result bit 0."""
    cpu = make_cpu()
    cpu.p |= CARRY_FLAG
    cpu.bus.write(0x0020, 0b0000_0010)

    rol(cpu, 0x0020)

    assert cpu.bus.read(0x0020) == 0b0000_0101
    assert (cpu.p & CARRY_FLAG) == 0


def test_rol_memory_sets_carry_from_old_bit_7():
    """Objective: old memory bit 7 becomes the new Carry flag."""
    cpu = make_cpu()
    cpu.bus.write(0x0020, 0b1000_0001)

    rol(cpu, 0x0020)

    assert cpu.bus.read(0x0020) == 0b0000_0010
    assert (cpu.p & CARRY_FLAG) != 0


def test_rol_memory_sets_zero_flag_when_result_is_zero():
    """Objective: 0x80 with old Carry=0 becomes 0x00 and sets Zero."""
    cpu = make_cpu()
    cpu.bus.write(0x0020, 0x80)

    rol(cpu, 0x0020)

    assert cpu.bus.read(0x0020) == 0x00
    assert (cpu.p & ZERO_FLAG) != 0
    assert (cpu.p & NEGATIVE_FLAG) == 0
    assert (cpu.p & CARRY_FLAG) != 0


def test_rol_memory_sets_negative_flag_from_result_bit_7():
    """Objective: 0x40 with old Carry=0 becomes 0x80 and sets Negative."""
    cpu = make_cpu()
    cpu.bus.write(0x0020, 0x40)

    rol(cpu, 0x0020)

    assert cpu.bus.read(0x0020) == 0x80
    assert (cpu.p & NEGATIVE_FLAG) != 0
    assert (cpu.p & ZERO_FLAG) == 0
