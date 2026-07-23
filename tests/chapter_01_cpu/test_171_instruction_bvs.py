"""
Add the BVS instruction behavior.

Instruction:
    BVS -> Branch if Overflow Set

Goal:
implement bvs(cpu, offset) in instructions.py.
"""

from emulator.cpu.instructions import bvs
from tests.helpers import make_cpu


def test_bvs_branches_when_overflow_flag_is_set():
    """Objective: if Overflow is set, PC is changed by the signed offset."""
    cpu = make_cpu()
    cpu.pc = 0x8002
    cpu.flags.set_overflow_flag(True)

    bvs(cpu, 0x05)

    assert cpu.pc == 0x8007


def test_bvs_does_not_branch_when_overflow_flag_is_clear():
    """Objective: if Overflow is clear, PC remains unchanged."""
    cpu = make_cpu()
    cpu.pc = 0x8002
    cpu.flags.set_overflow_flag(False)

    bvs(cpu, 0x05)

    assert cpu.pc == 0x8002
