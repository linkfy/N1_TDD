"""
Add the BVC instruction behavior.

Instruction:
    BVC -> Branch if Overflow Clear

Goal:
implement bvc(cpu, offset) in instructions.py.
"""

from emulator.cpu.instructions import bvc
from tests.helpers import make_cpu


def test_bvc_branches_when_overflow_flag_is_clear():
    """Objective: if Overflow is clear, PC is changed by the signed offset."""
    cpu = make_cpu()
    cpu.pc = 0x8002
    cpu.flags.set_overflow_flag(False)

    bvc(cpu, 0x05)

    assert cpu.pc == 0x8007


def test_bvc_does_not_branch_when_overflow_flag_is_set():
    """Objective: if Overflow is set, PC remains unchanged."""
    cpu = make_cpu()
    cpu.pc = 0x8002
    cpu.flags.set_overflow_flag(True)

    bvc(cpu, 0x05)

    assert cpu.pc == 0x8002
