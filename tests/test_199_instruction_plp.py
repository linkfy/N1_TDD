"""
Add the PLP instruction behavior.

Instruction:
    PLP -> Pull Processor Status

Goal:
implement plp(cpu) in instructions.py.

Student guidance:
PLP restores the processor status register P from the CPU stack.

6502 stack rule:
    Pull increments S first, then reads from the stack.

So if:
    S = $FC
    $01FD = saved status byte

Then PLP must:
    1. increment S to $FD
    2. read saved status from $01FD
    3. restore CPU flags from that byte

Important status-byte detail:
    In this emulator model, bits 4 and 5 are not kept as persistent CPU state.
    That matches the model already used by RTI:

        cpu.p = flags & 0b1100_1111

Common mistakes:
    - Reading before incrementing S.
    - Forgetting to mask out Break/unused bits.
    - Treating PLP like PLA and updating Z/N from a data value.

Implementation shape:

    cpu.s = (cpu.s + 1) & 0xFF
    flags = cpu.bus.read(0x0100 | cpu.s)
    cpu.p = flags & 0b1100_1111
"""

from emulator.cpu.instructions import plp
from tests.helpers import make_cpu


CARRY_FLAG = 1 << 0
ZERO_FLAG = 1 << 1
INTERRUPT_DISABLE_FLAG = 1 << 2
BREAK_FLAG = 1 << 5
OVERFLOW_FLAG = 1 << 6
NEGATIVE_FLAG = 1 << 7
STACK_BASE = 0x0100


def test_plp_pulls_status_from_stack_into_processor_status():
    """Objective: PLP restores status flags from $0100 | incremented S."""
    cpu = make_cpu()
    cpu.s = 0xFC
    saved_status = CARRY_FLAG | ZERO_FLAG | INTERRUPT_DISABLE_FLAG | OVERFLOW_FLAG | NEGATIVE_FLAG
    cpu.bus.write(STACK_BASE | 0xFD, saved_status)

    plp(cpu)

    assert cpu.p == saved_status


def test_plp_increments_stack_pointer_before_reading():
    """
    Objective:
    PLP must increment S before reading.

    With S = $FC, the pulled status comes from $01FD, not $01FC.
    """
    cpu = make_cpu()
    cpu.s = 0xFC
    cpu.bus.write(STACK_BASE | 0xFC, CARRY_FLAG)
    cpu.bus.write(STACK_BASE | 0xFD, NEGATIVE_FLAG)

    plp(cpu)

    assert cpu.p == NEGATIVE_FLAG
    assert cpu.s == 0xFD


def test_plp_restores_zero_and_negative_from_saved_status_bits():
    """
    Objective:
    PLP restores Z and N from the saved status byte.

    Unlike PLA, it does not compute Z/N from a pulled data value. It copies the
    saved flag bits.
    """
    cpu = make_cpu()
    cpu.s = 0xFC
    cpu.flags.set_zero_flag(False)
    cpu.flags.set_negative_flag(False)
    cpu.bus.write(STACK_BASE | 0xFD, ZERO_FLAG | NEGATIVE_FLAG)

    plp(cpu)

    assert cpu.flags.get_zero_flag() is True
    assert cpu.flags.get_negative_flag() is True


def test_plp_clears_break_and_unused_status_bits_from_pulled_status():
    """
    Objective:
    In this emulator model, bits 4 and 5 are not kept in cpu.p after PLP.

    PHP may push Break in the saved stack byte, but PLP should not keep Break as
    persistent CPU state.
    """
    cpu = make_cpu()
    cpu.s = 0xFC
    saved_status_with_break_and_unused = 0b0011_0000 | CARRY_FLAG | NEGATIVE_FLAG
    cpu.bus.write(STACK_BASE | 0xFD, saved_status_with_break_and_unused)

    plp(cpu)

    assert (cpu.p & BREAK_FLAG) == 0
    assert cpu.p == (CARRY_FLAG | NEGATIVE_FLAG)


def test_plp_replaces_previous_processor_status():
    """
    Objective:
    PLP restores P from the stack. It does not merge old flags with new flags.

    Failure mode this catches:
    Using cpu.p |= flags would leave stale flags set.
    """
    cpu = make_cpu()
    cpu.s = 0xFC
    cpu.p = CARRY_FLAG | ZERO_FLAG | OVERFLOW_FLAG | NEGATIVE_FLAG
    cpu.bus.write(STACK_BASE | 0xFD, INTERRUPT_DISABLE_FLAG)

    plp(cpu)

    assert cpu.p == INTERRUPT_DISABLE_FLAG


def test_plp_stack_pointer_wraps_to_8_bits():
    """Objective: S is an 8-bit stack pointer and wraps before reading."""
    cpu = make_cpu()
    cpu.s = 0xFF
    cpu.bus.write(STACK_BASE | 0x00, CARRY_FLAG | NEGATIVE_FLAG)

    plp(cpu)

    assert cpu.p == (CARRY_FLAG | NEGATIVE_FLAG)
    assert cpu.s == 0x00
