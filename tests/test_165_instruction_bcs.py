"""
Add the BCS instruction behavior.

Instruction:
    BCS -> Branch if Carry Set

Goal:
implement bcs(cpu, offset) in instructions.py.

Student guidance:
The offset is already signed by relative(cpu). BCS only checks Carry and, if
Carry is set, adds the offset to PC.

Remember:
PC is 16-bit, so branch targets must use `& 0xFFFF`.
"""

from emulator.cpu.instructions import bcs
from tests.helpers import make_cpu


def test_bcs_branches_when_carry_flag_is_set():
    """Objective: if Carry is set, PC is changed by the signed offset."""
    cpu = make_cpu()
    cpu.pc = 0x8002
    cpu.flags.set_carry_flag(True)

    bcs(cpu, 0x05)

    assert cpu.pc == 0x8007


def test_bcs_does_not_branch_when_carry_flag_is_clear():
    """Objective: if Carry is clear, PC remains unchanged."""
    cpu = make_cpu()
    cpu.pc = 0x8002
    cpu.flags.set_carry_flag(False)

    bcs(cpu, 0x05)

    assert cpu.pc == 0x8002


def test_bcs_wraps_pc_to_16_bits():
    """Objective: 0xFFFF + 1 wraps to 0x0000."""
    cpu = make_cpu()
    cpu.pc = 0xFFFF
    cpu.flags.set_carry_flag(True)

    bcs(cpu, 1)

    assert cpu.pc == 0x0000
