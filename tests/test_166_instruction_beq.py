"""
Add the BEQ instruction behavior.

Instruction:
    BEQ -> Branch if Equal

Goal:
implement beq(cpu, offset) in instructions.py.

Student guidance:
BEQ branches when Zero is set. The name comes from comparison instructions:
after CMP/CPX/CPY, Zero means the compared values were equal.
"""

from emulator.cpu.instructions import beq
from tests.helpers import make_cpu


def test_beq_branches_when_zero_flag_is_set():
    """Objective: if Zero is set, PC is changed by the signed offset."""
    cpu = make_cpu()
    cpu.pc = 0x8002
    cpu.flags.set_zero_flag(True)

    beq(cpu, 0x05)

    assert cpu.pc == 0x8007


def test_beq_does_not_branch_when_zero_flag_is_clear():
    """Objective: if Zero is clear, PC remains unchanged."""
    cpu = make_cpu()
    cpu.pc = 0x8002
    cpu.flags.set_zero_flag(False)

    beq(cpu, 0x05)

    assert cpu.pc == 0x8002


def test_beq_accepts_negative_signed_offsets():
    """Objective: offsets from relative(cpu) may be negative."""
    cpu = make_cpu()
    cpu.pc = 0x8002
    cpu.flags.set_zero_flag(True)

    beq(cpu, -2)

    assert cpu.pc == 0x8000
