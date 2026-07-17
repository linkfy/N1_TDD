"""
Expand FlagsHandler with Decimal flag helpers.

Why this step exists:
We are preparing for instructions that explicitly control the Decimal flag:

    SED -> Set Decimal Flag
    CLD -> Clear Decimal Flag

The 6502 status register has a Decimal flag at bit 3:

    NV-BDIZC
        ^
        D = Decimal flag

Important NES note:
The NES CPU has the Decimal flag bit, but decimal arithmetic mode is not used in
the same way as a full 6502 with BCD arithmetic. Even so, instructions like SED
and CLD still set and clear the flag bit, so our emulator needs helpers for it.

Design goal:
Keep raw bit manipulation inside FlagsHandler instead of spreading cpu.p masks
through instruction code.

Required API:
    set_decimal_flag(enabled: bool)
    get_decimal_flag() -> bool

Common mistake:
When clearing Decimal, use:

    cpu.p &= ~DECIMAL_FLAG

not:

    cpu.p &= DECIMAL_FLAG

The second version destroys all other flags.
"""

import inspect

from emulator.cpu.flags_handler import FlagsHandler
from tests.helpers import make_cpu


CARRY_FLAG = 1 << 0
ZERO_FLAG = 1 << 1
INTERRUPT_DISABLE_FLAG = 1 << 2
DECIMAL_FLAG = 1 << 3
OVERFLOW_FLAG = 1 << 6
NEGATIVE_FLAG = 1 << 7


def test_flags_handler_has_decimal_flag_helpers():
    """
    Objective:
    Add helpers for the Decimal flag.

    Required API:
        set_decimal_flag(enabled: bool)
        get_decimal_flag() -> bool

    Why:
    SED and CLD should not manipulate cpu.p directly. They should use
    FlagsHandler.
    """
    assert hasattr(FlagsHandler, "set_decimal_flag")
    assert hasattr(FlagsHandler, "get_decimal_flag")

    assert list(inspect.signature(FlagsHandler.set_decimal_flag).parameters) == [
        "self",
        "enabled",
    ]
    assert list(inspect.signature(FlagsHandler.get_decimal_flag).parameters) == ["self"]


def test_flags_handler_sets_and_clears_decimal_flag():
    """
    Objective:
    set_decimal_flag(True) sets bit 3.
    set_decimal_flag(False) clears bit 3.
    """
    cpu = make_cpu()

    cpu.flags.set_decimal_flag(True)
    assert (cpu.p & DECIMAL_FLAG) != 0
    assert cpu.flags.get_decimal_flag() is True

    cpu.flags.set_decimal_flag(False)
    assert (cpu.p & DECIMAL_FLAG) == 0
    assert cpu.flags.get_decimal_flag() is False


def test_clearing_decimal_flag_preserves_other_flags():
    """
    Objective:
    Clearing Decimal must not erase Carry, Zero, Interrupt Disable, Overflow, or
    Negative.

    Failure mode this catches:
        self.cpu.p &= DECIMAL_FLAG

    That keeps only the Decimal bit and clears everything else.
    """
    cpu = make_cpu()
    other_flags = CARRY_FLAG | ZERO_FLAG | INTERRUPT_DISABLE_FLAG | OVERFLOW_FLAG | NEGATIVE_FLAG
    cpu.p = other_flags | DECIMAL_FLAG

    cpu.flags.set_decimal_flag(False)

    assert (cpu.p & DECIMAL_FLAG) == 0
    assert (cpu.p & other_flags) == other_flags


def test_setting_decimal_flag_preserves_other_flags():
    """
    Objective:
    Setting Decimal must add bit 3 without damaging existing status flags.
    """
    cpu = make_cpu()
    other_flags = CARRY_FLAG | ZERO_FLAG | OVERFLOW_FLAG | NEGATIVE_FLAG
    cpu.p = other_flags

    cpu.flags.set_decimal_flag(True)

    assert (cpu.p & DECIMAL_FLAG) != 0
    assert (cpu.p & other_flags) == other_flags


def test_decimal_flag_is_independent_from_interrupt_disable_flag():
    """
    Objective:
    Decimal and Interrupt Disable are neighboring bits, but they are different
    flags.

        I flag = bit 2
        D flag = bit 3

    Setting or clearing one must not toggle the other.
    """
    cpu = make_cpu()

    cpu.flags.set_interrupt_disable_flag(True)
    assert cpu.flags.get_interrupt_disable_flag() is True
    assert cpu.flags.get_decimal_flag() is False

    cpu.flags.set_decimal_flag(True)
    assert cpu.flags.get_interrupt_disable_flag() is True
    assert cpu.flags.get_decimal_flag() is True

    cpu.flags.set_decimal_flag(False)
    assert cpu.flags.get_interrupt_disable_flag() is True
    assert cpu.flags.get_decimal_flag() is False
