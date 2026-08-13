"""
Add the RTI instruction behavior.

Instruction:
    RTI -> Return from Interrupt

Goal:
implement rti(cpu) in instructions.py.

Student guidance:
RTI is the matching return instruction for interrupt handling.

BRK/interrupt entry pushes three bytes to the stack:

    1. return PC high byte
    2. return PC low byte
    3. processor status flags

Because the 6502 stack is last-in, first-out, RTI pulls them back in the
opposite order:

    1. status flags
    2. PC low byte
    3. PC high byte

Important difference from RTS:
    RTS pulls an address and then adds 1.
    RTI restores the exact PC from the stack. It does not add 1.

Example stack before RTI:

    S = $FA
    $01FB = $85    saved status flags
    $01FC = $34    return PC low byte
    $01FD = $12    return PC high byte

After RTI:

    P  = $85 with bits 4 and 5 cleared in this emulator model
    PC = $1234
    S  = $FD

Implementation shape:

    cpu.s = (cpu.s + 1) & 0xFF
    flags = cpu.bus.read(0x0100 | cpu.s)
    cpu.p = flags & 0b1100_1111

    cpu.s = (cpu.s + 1) & 0xFF
    low = cpu.bus.read(0x0100 | cpu.s)

    cpu.s = (cpu.s + 1) & 0xFF
    high = cpu.bus.read(0x0100 | cpu.s)

    cpu.pc = (high << 8) | low

Common mistakes:
    - Pulling PC before status.
    - Adding 1 to PC like RTS.
    - Reading stack before incrementing S.
    - Keeping Break as persistent CPU state after RTI.
"""

from emulator.cpu.instructions import rti
from tests.helpers import make_cpu


CARRY_FLAG = 1 << 0
ZERO_FLAG = 1 << 1
INTERRUPT_DISABLE_FLAG = 1 << 2
BREAK_FLAG = 1 << 4
ONE_FLAG = 1 << 5
OVERFLOW_FLAG = 1 << 6
NEGATIVE_FLAG = 1 << 7
STACK_BASE = 0x0100


def test_rti_restores_program_counter_from_stack_without_adding_one():
    """
    Objective:
    RTI restores the exact PC from the stack.

    If the stack contains $1234, PC becomes $1234, not $1235.
    """
    cpu = make_cpu()
    cpu.s = 0xFA
    cpu.bus.write(STACK_BASE | 0xFB, 0x00)
    cpu.bus.write(STACK_BASE | 0xFC, 0x34)
    cpu.bus.write(STACK_BASE | 0xFD, 0x12)

    rti(cpu)

    assert cpu.pc == 0x1234


def test_rti_pulls_status_then_pc_low_then_pc_high():
    """
    Objective:
    RTI must pull stack bytes in interrupt-return order:

        status -> PC low -> PC high

    This is the reverse of what BRK/interrupt entry pushed.
    """
    cpu = make_cpu()
    cpu.s = 0xFA
    cpu.bus.write(STACK_BASE | 0xFB, CARRY_FLAG | NEGATIVE_FLAG)
    cpu.bus.write(STACK_BASE | 0xFC, 0xCD)
    cpu.bus.write(STACK_BASE | 0xFD, 0xAB)

    rti(cpu)

    assert cpu.p == (CARRY_FLAG | NEGATIVE_FLAG)
    assert cpu.pc == 0xABCD


def test_rti_increments_stack_pointer_three_times():
    """Objective: RTI pulls status, PC low, and PC high, so S increases by 3."""
    cpu = make_cpu()
    cpu.s = 0xFA
    cpu.bus.write(STACK_BASE | 0xFB, 0x00)
    cpu.bus.write(STACK_BASE | 0xFC, 0x34)
    cpu.bus.write(STACK_BASE | 0xFD, 0x12)

    rti(cpu)

    assert cpu.s == 0xFD


def test_rti_restores_status_flags_from_stack():
    """
    Objective:
    RTI restores saved processor status flags from the stack.

    These flags affect later branches and arithmetic, so RTI must not leave the
    interrupt handler's temporary flags behind.
    """
    cpu = make_cpu()
    cpu.s = 0xFA
    saved_flags = CARRY_FLAG | ZERO_FLAG | INTERRUPT_DISABLE_FLAG | OVERFLOW_FLAG | NEGATIVE_FLAG
    cpu.bus.write(STACK_BASE | 0xFB, saved_flags)
    cpu.bus.write(STACK_BASE | 0xFC, 0x34)
    cpu.bus.write(STACK_BASE | 0xFD, 0x12)

    rti(cpu)

    assert cpu.p == saved_flags


def test_rti_clears_break_and_unused_status_bits_from_pulled_status():
    """
    Objective:
    In this emulator model, status bits 4 and 5 are not kept as persistent CPU
    state after RTI.

    Why:
    BRK may push a status byte with Break set, but Break is metadata in the
    saved stack byte, not a normal long-lived CPU flag here.
    """
    cpu = make_cpu()
    cpu.s = 0xFA
    saved_flags_with_break_and_unused = 0b0011_0000 | CARRY_FLAG | NEGATIVE_FLAG
    cpu.bus.write(STACK_BASE | 0xFB, saved_flags_with_break_and_unused)
    cpu.bus.write(STACK_BASE | 0xFC, 0x34)
    cpu.bus.write(STACK_BASE | 0xFD, 0x12)

    rti(cpu)

    assert (cpu.p & BREAK_FLAG) == 0
    assert (cpu.p & ONE_FLAG) == 0
    assert cpu.p == (CARRY_FLAG | NEGATIVE_FLAG)


def test_rti_stack_pointer_wraps_to_8_bits():
    """Objective: S is an 8-bit stack pointer and wraps while pulling bytes."""
    cpu = make_cpu()
    cpu.s = 0xFE
    cpu.bus.write(STACK_BASE | 0xFF, CARRY_FLAG)
    cpu.bus.write(STACK_BASE | 0x00, 0x78)
    cpu.bus.write(STACK_BASE | 0x01, 0x56)

    rti(cpu)

    assert cpu.p == CARRY_FLAG
    assert cpu.pc == 0x5678
    assert cpu.s == 0x01
