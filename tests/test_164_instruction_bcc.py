"""
Add the BCC instruction behavior.

Instruction:
    BCC -> Branch if Carry Clear

Goal:
implement bcc(cpu, offset) in instructions.py.

Student guidance:
The offset is already signed by relative(cpu). BCC only decides whether to add
that offset to PC.

Important:
PC is a 16-bit register. When the branch is taken, remember to keep PC inside
0x0000..0xFFFF:

    cpu.pc = (cpu.pc + offset) & 0xFFFF

Without `& 0xFFFF`, branching near the beginning or end of memory can produce
an invalid PC value.
"""

from emulator.cpu.instructions import bcc
from tests.helpers import make_cpu


def test_bcc_branches_when_carry_flag_is_clear():
    """Objective: if Carry is clear, PC is changed by the signed offset."""
    cpu = make_cpu()
    cpu.pc = 0x8002
    cpu.flags.set_carry_flag(False)

    bcc(cpu, 0x05)

    assert cpu.pc == 0x8007


def test_bcc_does_not_branch_when_carry_flag_is_set():
    """Objective: if Carry is set, PC remains unchanged."""
    cpu = make_cpu()
    cpu.pc = 0x8002
    cpu.flags.set_carry_flag(True)

    bcc(cpu, 0x05)

    assert cpu.pc == 0x8002


def test_bcc_accepts_negative_signed_offsets():
    """Objective: offsets from relative(cpu) may be negative, such as -2."""
    cpu = make_cpu()
    cpu.pc = 0x8002
    cpu.flags.set_carry_flag(False)

    bcc(cpu, -2)

    assert cpu.pc == 0x8000


def test_bcc_wraps_pc_to_16_bits_when_branch_underflows():
    """
    Objective:
    PC must stay 16-bit after adding the offset.

    Example:
    0x0001 + (-2) should become 0xFFFF, not -1.

    Hint:
    Use `& 0xFFFF` after adding the offset.
    """
    cpu = make_cpu()
    cpu.pc = 0x0001
    cpu.flags.set_carry_flag(False)

    bcc(cpu, -2)

    assert cpu.pc == 0xFFFF


def test_bcc_wraps_pc_to_16_bits_when_branch_overflows():
    """
    Objective:
    PC must also wrap when the addition goes past 0xFFFF.

    Example:
    0xFFFF + 1 should become 0x0000.

    Hint:
    This is the same `& 0xFFFF` invariant.
    """
    cpu = make_cpu()
    cpu.pc = 0xFFFF
    cpu.flags.set_carry_flag(False)

    bcc(cpu, 1)

    assert cpu.pc == 0x0000
