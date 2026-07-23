"""
Add the TXS instruction behavior.

Instruction:
    TXS -> Transfer X to Stack Pointer

Goal:
implement txs(cpu) in instructions.py.

Student guidance:
TXS copies register X into the stack pointer S.

Important details:
    - S is the low byte of the CPU stack address.
    - The actual stack page is still $0100-$01FF.
    - TXS only changes S.
    - TXS does not change X.
    - TXS does not update status flags.

Example:
    X = $80
    S = $FD

After TXS:
    X = $80
    S = $80

Common mistake:
Do not update Zero or Negative flags. Unlike TAX/TXA/TAY/TYA, TXS does not
modify flags on the 6502.

Implementation shape:

    cpu.s = cpu.x
"""

from emulator.cpu.instructions import txs
from tests.helpers import NEGATIVE_FLAG, ZERO_FLAG, make_cpu


CARRY_FLAG = 1 << 0
OVERFLOW_FLAG = 1 << 6


def test_txs_copies_x_to_stack_pointer():
    """Objective: TXS sets S to the current value of X."""
    cpu = make_cpu()
    cpu.x = 0x80
    cpu.s = 0xFD

    txs(cpu)

    assert cpu.s == 0x80


def test_txs_does_not_modify_x():
    """Objective: TXS copies X but leaves X unchanged."""
    cpu = make_cpu()
    cpu.x = 0x42
    cpu.s = 0xFD

    txs(cpu)

    assert cpu.x == 0x42


def test_txs_can_set_stack_pointer_to_zero_without_setting_zero_flag():
    """
    Objective:
    TXS does not update Zero, even if X is $00.
    """
    cpu = make_cpu()
    cpu.x = 0x00
    cpu.s = 0xFD
    cpu.flags.set_zero_flag(False)

    txs(cpu)

    assert cpu.s == 0x00
    assert cpu.flags.get_zero_flag() is False


def test_txs_can_set_stack_pointer_to_negative_value_without_setting_negative_flag():
    """
    Objective:
    TXS does not update Negative, even if bit 7 of X is set.
    """
    cpu = make_cpu()
    cpu.x = 0x80
    cpu.s = 0xFD
    cpu.flags.set_negative_flag(False)

    txs(cpu)

    assert cpu.s == 0x80
    assert cpu.flags.get_negative_flag() is False


def test_txs_preserves_all_status_flags():
    """Objective: TXS is a register transfer to S and does not change flags."""
    cpu = make_cpu()
    cpu.x = 0x12
    cpu.s = 0xFD
    cpu.p = CARRY_FLAG | ZERO_FLAG | OVERFLOW_FLAG | NEGATIVE_FLAG

    txs(cpu)

    assert cpu.p == (CARRY_FLAG | ZERO_FLAG | OVERFLOW_FLAG | NEGATIVE_FLAG)
