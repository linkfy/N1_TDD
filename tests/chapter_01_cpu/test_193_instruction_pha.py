"""
Add the PHA instruction behavior.

Instruction:
    PHA -> Push Accumulator

Goal:
implement pha(cpu) in instructions.py.

Student guidance:
PHA saves the current value of register A on the CPU stack.

6502 stack rule:
    Push writes first, then decrements S.

So if:
    A = $42
    S = $FD

Then PHA must:
    1. write $42 to $01FD
    2. decrement S to $FC

Important details:
    - The stack lives in page $0100-$01FF.
    - S is only the low byte of the stack address.
    - PHA pushes A exactly as it is.
    - PHA does not modify A.
    - PHA does not modify status flags.

Common mistake:
Do not decrement S before writing. That would store A at the wrong stack slot.

Implementation shape:

    cpu.bus.write(0x0100 | cpu.s, cpu.a)
    cpu.s = (cpu.s - 1) & 0xFF
"""

from emulator.cpu.instructions import pha
from tests.helpers import NEGATIVE_FLAG, ZERO_FLAG, make_cpu


CARRY_FLAG = 1 << 0
INTERRUPT_DISABLE_FLAG = 1 << 2
OVERFLOW_FLAG = 1 << 6
STACK_BASE = 0x0100


def test_pha_pushes_accumulator_to_current_stack_address():
    """Objective: PHA writes A to $0100 | S before changing S."""
    cpu = make_cpu()
    cpu.a = 0x42
    cpu.s = 0xFD

    pha(cpu)

    assert cpu.bus.read(STACK_BASE | 0xFD) == 0x42


def test_pha_decrements_stack_pointer_after_push():
    """Objective: after one push, S decreases by 1."""
    cpu = make_cpu()
    cpu.a = 0x42
    cpu.s = 0xFD

    pha(cpu)

    assert cpu.s == 0xFC


def test_pha_does_not_modify_accumulator():
    """Objective: PHA copies A to the stack but leaves A unchanged."""
    cpu = make_cpu()
    cpu.a = 0x99
    cpu.s = 0xFD

    pha(cpu)

    assert cpu.a == 0x99


def test_pha_stack_pointer_wraps_to_8_bits():
    """Objective: S is an 8-bit stack pointer and wraps after decrementing."""
    cpu = make_cpu()
    cpu.a = 0xAB
    cpu.s = 0x00

    pha(cpu)

    assert cpu.bus.read(STACK_BASE | 0x00) == 0xAB
    assert cpu.s == 0xFF


def test_pha_can_push_zero_value_without_setting_zero_flag():
    """
    Objective:
    PHA is a stack transfer, not an arithmetic/load instruction.

    Even if A is $00, PHA must not update the Zero flag.
    """
    cpu = make_cpu()
    cpu.a = 0x00
    cpu.s = 0xFD
    cpu.flags.set_zero_flag(False)

    pha(cpu)

    assert cpu.bus.read(STACK_BASE | 0xFD) == 0x00
    assert cpu.flags.get_zero_flag() is False


def test_pha_can_push_negative_value_without_setting_negative_flag():
    """
    Objective:
    PHA must not update Negative based on bit 7 of A.

    It only saves A to stack.
    """
    cpu = make_cpu()
    cpu.a = 0x80
    cpu.s = 0xFD
    cpu.flags.set_negative_flag(False)

    pha(cpu)

    assert cpu.bus.read(STACK_BASE | 0xFD) == 0x80
    assert cpu.flags.get_negative_flag() is False


def test_pha_preserves_status_flags():
    """Objective: PHA does not modify any processor status flags."""
    cpu = make_cpu()
    cpu.a = 0x42
    cpu.s = 0xFD
    cpu.p = CARRY_FLAG | ZERO_FLAG | INTERRUPT_DISABLE_FLAG | OVERFLOW_FLAG | NEGATIVE_FLAG

    pha(cpu)

    assert cpu.p == (CARRY_FLAG | ZERO_FLAG | INTERRUPT_DISABLE_FLAG | OVERFLOW_FLAG | NEGATIVE_FLAG)
