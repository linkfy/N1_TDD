"""
Add a new instruction: INC.

INC means Increment Memory.

Create one function inside emulator/cpu/instructions.py:

    def inc(cpu, address):
        ...

Goal:
read one byte from memory, add 1, write it back to the same address,
and update Zero/Negative flags.

Reference:
https://www.nesdev.org/wiki/Instruction_reference#INC
"""
import inspect

from tests.helpers import NEGATIVE_FLAG, ZERO_FLAG, make_cpu
from emulator.cpu import instructions


def test_inc_instruction_exists():
    """
    Objective:
    Create in instructions.py:
        def inc(cpu, address):
            ...

    Implementation shape:
        value = cpu.bus.read(address)
        result = value + 1
        result_8 = result & 0xFF

        cpu.bus.write(address, result_8)
        cpu.flags.set_zero_flag(result_8 == 0)
        cpu.flags.set_negative_flag((result_8 & 0x80) != 0)

    Important:
    INC receives an address, not a value.
    INC modifies memory, not A/X/Y directly.
    """
    assert hasattr(instructions, "inc")
    assert callable(instructions.inc)
    assert list(inspect.signature(instructions.inc).parameters) == ["cpu", "address"]


def test_inc_reads_memory_adds_one_and_writes_back():
    """
    Objective:
    inc(cpu, address) must increment the value stored at that address.

    Example:
    RAM[$0010] is 0x41.
    After INC, RAM[$0010] becomes 0x42.
    """
    cpu = make_cpu()
    cpu.bus.write(0x0010, 0x41)

    instructions.inc(cpu, 0x0010)

    assert cpu.bus.read(0x0010) == 0x42


def test_inc_wraps_from_ff_to_zero_and_sets_zero_flag():
    """
    Objective:
    INC works with 8-bit values.

    Example:
    0xFF + 1 becomes 0x00.
    Zero flag is set.
    """
    cpu = make_cpu()
    cpu.bus.write(0x0010, 0xFF)

    instructions.inc(cpu, 0x0010)

    assert cpu.bus.read(0x0010) == 0x00
    assert (cpu.p & ZERO_FLAG) != 0
    assert (cpu.p & NEGATIVE_FLAG) == 0


def test_inc_sets_negative_flag_when_result_has_bit_7_active():
    """
    Objective:
    INC updates the Negative flag from bit 7 of the result.

    Example:
    0x7F + 1 becomes 0x80.
    0x80 has bit 7 active, so Negative flag is set.
    """
    cpu = make_cpu()
    cpu.bus.write(0x0010, 0x7F)

    instructions.inc(cpu, 0x0010)

    assert cpu.bus.read(0x0010) == 0x80
    assert (cpu.p & NEGATIVE_FLAG) != 0
    assert (cpu.p & ZERO_FLAG) == 0


def test_inc_does_not_change_carry_or_overflow_flags():
    """
    Objective:
    INC only updates Zero and Negative flags.

    It must not modify Carry or Overflow.
    """
    cpu = make_cpu()
    cpu.bus.write(0x0010, 0x01)
    cpu.flags.set_carry_flag(True)
    cpu.flags.set_overflow_flag(True)

    instructions.inc(cpu, 0x0010)

    assert cpu.bus.read(0x0010) == 0x02
    assert cpu.flags.get_carry_flag() is True
    assert cpu.flags.get_overflow_flag() is True
