"""
Add the LSR memory instruction behavior.

Instruction:
    LSR memory -> memory[address] = memory[address] >> 1

Goal:
implement lsr(cpu, address) in instructions.py for memory destinations.

Student guidance:
LSR shifts right. The old bit 0 is the bit that falls out, so it becomes
Carry. Bit 7 is filled with 0, so Negative is always cleared.
"""

from emulator.cpu.instructions import lsr
from tests.helpers import NEGATIVE_FLAG, ZERO_FLAG, make_cpu


CARRY_FLAG = 1 << 0


def test_lsr_memory_shifts_value_right_and_writes_result_back():
    """Objective: memory value 0b0000_0110 becomes 0b0000_0011."""
    cpu = make_cpu()
    cpu.bus.write(0x0020, 0b0000_0110)

    lsr(cpu, 0x0020)

    assert cpu.bus.read(0x0020) == 0b0000_0011


def test_lsr_memory_sets_carry_from_old_bit_0():
    """Objective: old bit 0 is moved into Carry before the right shift."""
    cpu = make_cpu()
    cpu.bus.write(0x0020, 0b0000_0011)

    lsr(cpu, 0x0020)

    assert cpu.bus.read(0x0020) == 0b0000_0001
    assert (cpu.p & CARRY_FLAG) != 0


def test_lsr_memory_clears_carry_when_old_bit_0_was_clear():
    """Objective: Carry is cleared when the original value did not have bit 0 set."""
    cpu = make_cpu()
    cpu.p |= CARRY_FLAG
    cpu.bus.write(0x0020, 0b0000_0010)

    lsr(cpu, 0x0020)

    assert cpu.bus.read(0x0020) == 0b0000_0001
    assert (cpu.p & CARRY_FLAG) == 0


def test_lsr_memory_sets_zero_flag_when_result_is_zero():
    """Objective: 0x01 >> 1 becomes 0x00 and sets Zero flag."""
    cpu = make_cpu()
    cpu.bus.write(0x0020, 0x01)

    lsr(cpu, 0x0020)

    assert cpu.bus.read(0x0020) == 0x00
    assert (cpu.p & ZERO_FLAG) != 0


def test_lsr_memory_always_clears_negative_flag():
    """Objective: LSR fills bit 7 with 0, so Negative must be cleared."""
    cpu = make_cpu()
    cpu.p |= NEGATIVE_FLAG
    cpu.bus.write(0x0020, 0x80)

    lsr(cpu, 0x0020)

    assert cpu.bus.read(0x0020) == 0x40
    assert (cpu.p & NEGATIVE_FLAG) == 0
