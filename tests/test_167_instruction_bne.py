"""
Add the BNE instruction behavior.

Instruction:
    BNE -> Branch if Not Equal

Goal:
implement bne(cpu, offset) in instructions.py.

Student guidance:
BNE branches when Zero is clear. After CMP/CPX/CPY, Zero clear means the
compared values were not equal.
"""

from emulator.cpu.instructions import bne
from tests.helpers import make_cpu


def test_bne_branches_when_zero_flag_is_clear():
    """Objective: if Zero is clear, PC is changed by the signed offset."""
    cpu = make_cpu()
    cpu.pc = 0x8002
    cpu.flags.set_zero_flag(False)

    bne(cpu, 0x05)

    assert cpu.pc == 0x8007


def test_bne_does_not_branch_when_zero_flag_is_set():
    """Objective: if Zero is set, PC remains unchanged."""
    cpu = make_cpu()
    cpu.pc = 0x8002
    cpu.flags.set_zero_flag(True)

    bne(cpu, 0x05)

    assert cpu.pc == 0x8002


def test_bne_wraps_pc_to_16_bits():
    """Objective: 0x0001 + (-2) wraps to 0xFFFF."""
    cpu = make_cpu()
    cpu.pc = 0x0001
    cpu.flags.set_zero_flag(False)

    bne(cpu, -2)

    assert cpu.pc == 0xFFFF
