"""
Add the ASL memory instruction behavior.

Instruction:
    ASL memory -> memory[address] = memory[address] << 1

Goal:
implement asl(cpu, address) in instructions.py for memory destinations.

Important:
ASL stores old bit 7 into Carry, then writes the 8-bit shifted result back
to memory. Zero and Negative are based on the final 8-bit result.
"""

from emulator.cpu.instructions import asl
from tests.helpers import NEGATIVE_FLAG, ZERO_FLAG, make_cpu


CARRY_FLAG = 1 << 0


def test_asl_memory_shifts_value_left_and_writes_result_back():
    """Objective: memory value 0b0000_0011 becomes 0b0000_0110."""
    cpu = make_cpu()
    cpu.bus.write(0x0020, 0b0000_0011)

    asl(cpu, 0x0020)

    assert cpu.bus.read(0x0020) == 0b0000_0110


def test_asl_memory_sets_carry_from_old_bit_7():
    """Objective: old bit 7 is moved into Carry before the 8-bit wrap."""
    cpu = make_cpu()
    cpu.bus.write(0x0020, 0b1000_0001)

    asl(cpu, 0x0020)

    assert cpu.bus.read(0x0020) == 0b0000_0010
    assert (cpu.p & CARRY_FLAG) != 0


def test_asl_memory_clears_carry_when_old_bit_7_was_clear():
    """Objective: Carry is cleared when the original value did not have bit 7 set."""
    cpu = make_cpu()
    cpu.p |= CARRY_FLAG
    cpu.bus.write(0x0020, 0b0100_0000)

    asl(cpu, 0x0020)

    assert cpu.bus.read(0x0020) == 0b1000_0000
    assert (cpu.p & CARRY_FLAG) == 0


def test_asl_memory_sets_zero_flag_when_result_is_zero():
    """Objective: 0x80 << 1 becomes 0x00 and sets Zero flag."""
    cpu = make_cpu()
    cpu.bus.write(0x0020, 0x80)

    asl(cpu, 0x0020)

    assert cpu.bus.read(0x0020) == 0x00
    assert (cpu.p & ZERO_FLAG) != 0
    assert (cpu.p & NEGATIVE_FLAG) == 0


def test_asl_memory_sets_negative_flag_from_result_bit_7():
    """Objective: 0x40 << 1 becomes 0x80, so Negative flag is set."""
    cpu = make_cpu()
    cpu.bus.write(0x0020, 0x40)

    asl(cpu, 0x0020)

    assert cpu.bus.read(0x0020) == 0x80
    assert (cpu.p & NEGATIVE_FLAG) != 0
    assert (cpu.p & ZERO_FLAG) == 0
