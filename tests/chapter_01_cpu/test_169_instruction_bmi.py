"""
Add the BMI instruction behavior.

Instruction:
    BMI -> Branch if Minus

Goal:
implement bmi(cpu, offset) in instructions.py.

Student guidance:
In 6502 terminology, "minus" means Negative flag is set.
"""

from emulator.cpu.instructions import bmi
from tests.helpers import make_cpu


def test_bmi_branches_when_negative_flag_is_set():
    """Objective: if Negative is set, PC is changed by the signed offset."""
    cpu = make_cpu()
    cpu.pc = 0x8002
    cpu.flags.set_negative_flag(True)

    bmi(cpu, 0x05)

    assert cpu.pc == 0x8007


def test_bmi_does_not_branch_when_negative_flag_is_clear():
    """Objective: if Negative is clear, PC remains unchanged."""
    cpu = make_cpu()
    cpu.pc = 0x8002
    cpu.flags.set_negative_flag(False)

    bmi(cpu, 0x05)

    assert cpu.pc == 0x8002
