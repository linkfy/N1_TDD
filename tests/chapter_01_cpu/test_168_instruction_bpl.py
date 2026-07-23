"""
Add the BPL instruction behavior.

Instruction:
    BPL -> Branch if Plus

Goal:
implement bpl(cpu, offset) in instructions.py.

Student guidance:
In 6502 terminology, "plus" means Negative flag is clear.
"""

from emulator.cpu.instructions import bpl
from tests.helpers import make_cpu


def test_bpl_branches_when_negative_flag_is_clear():
    """Objective: if Negative is clear, PC is changed by the signed offset."""
    cpu = make_cpu()
    cpu.pc = 0x8002
    cpu.flags.set_negative_flag(False)

    bpl(cpu, 0x05)

    assert cpu.pc == 0x8007


def test_bpl_does_not_branch_when_negative_flag_is_set():
    """Objective: if Negative is set, PC remains unchanged."""
    cpu = make_cpu()
    cpu.pc = 0x8002
    cpu.flags.set_negative_flag(True)

    bpl(cpu, 0x05)

    assert cpu.pc == 0x8002
