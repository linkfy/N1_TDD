"""
Add the flag-control instruction behavior.

Instructions:
    CLC -> Clear Carry flag
    SEC -> Set Carry flag
    CLI -> Clear Interrupt Disable flag
    SEI -> Set Interrupt Disable flag
    CLD -> Clear Decimal flag
    SED -> Set Decimal flag
    CLV -> Clear Overflow flag

Goal:
implement these functions in instructions.py:

    clc(cpu)
    sec(cpu)
    cli(cpu)
    sei(cpu)
    cld(cpu)
    sed(cpu)
    clv(cpu)

Student guidance:
These instructions are small but important. Each one changes exactly one status
flag and should leave all other CPU state untouched.

Mental model:
    CLC/SEC control Carry.
    CLI/SEI control Interrupt Disable.
    CLD/SED control Decimal.
    CLV clears Overflow.

Important NES note:
The NES CPU still has the Decimal flag bit and SED/CLD still modify it, even
though decimal arithmetic mode is not used like on a full BCD 6502.

Common mistakes:
    - Updating Zero/Negative accidentally.
    - Clearing all flags instead of only one flag.
    - Confusing CLI with "clear interrupt happened". CLI clears Interrupt Disable.
    - Confusing CLV with a generic flag reset. CLV clears only Overflow.
"""

from emulator.cpu.instructions import clc, cld, cli, clv, sec, sed, sei
from tests.helpers import make_cpu


CARRY_FLAG = 1 << 0
ZERO_FLAG = 1 << 1
INTERRUPT_DISABLE_FLAG = 1 << 2
DECIMAL_FLAG = 1 << 3
OVERFLOW_FLAG = 1 << 6
NEGATIVE_FLAG = 1 << 7


def test_clc_clears_carry_flag_only():
    """Objective: CLC clears Carry and preserves other flags."""
    cpu = make_cpu()
    cpu.p = CARRY_FLAG | ZERO_FLAG | NEGATIVE_FLAG

    clc(cpu)

    assert cpu.flags.get_carry_flag() is False
    assert (cpu.p & ZERO_FLAG) != 0
    assert (cpu.p & NEGATIVE_FLAG) != 0


def test_sec_sets_carry_flag_only():
    """Objective: SEC sets Carry and preserves other flags."""
    cpu = make_cpu()
    cpu.p = ZERO_FLAG | NEGATIVE_FLAG

    sec(cpu)

    assert cpu.flags.get_carry_flag() is True
    assert (cpu.p & ZERO_FLAG) != 0
    assert (cpu.p & NEGATIVE_FLAG) != 0


def test_cli_clears_interrupt_disable_flag_only():
    """
    Objective:
    CLI clears the Interrupt Disable flag.

    Meaning:
    After CLI, maskable IRQ interrupts are allowed again.
    """
    cpu = make_cpu()
    cpu.p = INTERRUPT_DISABLE_FLAG | CARRY_FLAG | NEGATIVE_FLAG

    cli(cpu)

    assert cpu.flags.get_interrupt_disable_flag() is False
    assert (cpu.p & CARRY_FLAG) != 0
    assert (cpu.p & NEGATIVE_FLAG) != 0


def test_sei_sets_interrupt_disable_flag_only():
    """
    Objective:
    SEI sets the Interrupt Disable flag.

    Meaning:
    After SEI, maskable IRQ interrupts are disabled.
    """
    cpu = make_cpu()
    cpu.p = CARRY_FLAG | NEGATIVE_FLAG

    sei(cpu)

    assert cpu.flags.get_interrupt_disable_flag() is True
    assert (cpu.p & CARRY_FLAG) != 0
    assert (cpu.p & NEGATIVE_FLAG) != 0


def test_cld_clears_decimal_flag_only():
    """Objective: CLD clears Decimal and preserves other flags."""
    cpu = make_cpu()
    cpu.p = DECIMAL_FLAG | CARRY_FLAG | OVERFLOW_FLAG | NEGATIVE_FLAG

    cld(cpu)

    assert cpu.flags.get_decimal_flag() is False
    assert (cpu.p & CARRY_FLAG) != 0
    assert (cpu.p & OVERFLOW_FLAG) != 0
    assert (cpu.p & NEGATIVE_FLAG) != 0


def test_sed_sets_decimal_flag_only():
    """Objective: SED sets Decimal and preserves other flags."""
    cpu = make_cpu()
    cpu.p = CARRY_FLAG | OVERFLOW_FLAG | NEGATIVE_FLAG

    sed(cpu)

    assert cpu.flags.get_decimal_flag() is True
    assert (cpu.p & CARRY_FLAG) != 0
    assert (cpu.p & OVERFLOW_FLAG) != 0
    assert (cpu.p & NEGATIVE_FLAG) != 0


def test_clv_clears_overflow_flag_only():
    """Objective: CLV clears Overflow and preserves other flags."""
    cpu = make_cpu()
    cpu.p = OVERFLOW_FLAG | CARRY_FLAG | ZERO_FLAG | NEGATIVE_FLAG

    clv(cpu)

    assert cpu.flags.get_overflow_flag() is False
    assert (cpu.p & CARRY_FLAG) != 0
    assert (cpu.p & ZERO_FLAG) != 0
    assert (cpu.p & NEGATIVE_FLAG) != 0


def test_flag_control_instructions_do_not_modify_registers_or_stack_pointer():
    """
    Objective:
    Flag-control instructions should only change status flags.

    They must not modify A, X, Y, S, or PC.
    """
    for instruction in (clc, sec, cli, sei, cld, sed, clv):
        cpu = make_cpu()
        cpu.a = 0x11
        cpu.x = 0x22
        cpu.y = 0x33
        cpu.s = 0xFD
        cpu.pc = 0x8000

        instruction(cpu)

        assert cpu.a == 0x11
        assert cpu.x == 0x22
        assert cpu.y == 0x33
        assert cpu.s == 0xFD
        assert cpu.pc == 0x8000
