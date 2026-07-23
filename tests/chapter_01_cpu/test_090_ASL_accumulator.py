"""
Add ASL Accumulator.

Opcode:
    0x0A -> ASL A

Goal:
map opcode 0x0A directly to asl_a(cpu).

Student guidance:
ASL A is a special ASL form because it does not decode a memory address.
The destination is the accumulator register itself, so the opcode handler can
call asl_a(cpu) directly.

Important:
Do not use zero_page(cpu), absolute(cpu), or any other addressing helper here.
Opcode 0x0A is one byte long, so PC advances by exactly 1.
"""
import inspect

from emulator.bus.cpu_bus import CpuBus
from emulator.cpu import opcodes
from emulator.cpu.cpu import CPU
from emulator.memory.fake_rom import FakeROM
from tests.helpers import NEGATIVE_FLAG, ZERO_FLAG


CARRY_FLAG = 1 << 0


def make_cpu_with_rom():
    rom = FakeROM()
    rom.write(0x7FFC, 0x00)
    rom.write(0x7FFD, 0x80)
    bus = CpuBus(program_rom=rom)
    return CPU(bus), bus, rom


def test_asl_accumulator_opcode_exists_and_is_in_opcode_table():
    """Objective: import asl_a and add 0x0A to OPCODE_TABLE."""
    assert hasattr(opcodes, "asl_a")
    assert callable(opcodes.asl_a)
    assert list(inspect.signature(opcodes.asl_a).parameters) == ["cpu"]
    assert opcodes.OPCODE_TABLE[0x0A] is opcodes.asl_a


def test_opcode_0A_asl_accumulator_shifts_a_and_advances_pc_by_one():
    """Objective: 0A means ASL A, so only A is shifted and PC advances by 1."""
    cpu, bus, rom = make_cpu_with_rom()
    rom.write(0x0000, 0x0A)

    cpu.reset()
    cpu.a = 0b0000_0011
    cpu.step()

    assert cpu.a == 0b0000_0110
    assert cpu.pc == 0x8001


def test_opcode_0A_asl_accumulator_sets_carry_from_old_a_bit_7():
    """Objective: old A bit 7 is copied into Carry before the result wraps."""
    cpu, bus, rom = make_cpu_with_rom()
    rom.write(0x0000, 0x0A)

    cpu.reset()
    cpu.a = 0b1000_0001
    cpu.step()

    assert cpu.a == 0b0000_0010
    assert (cpu.p & CARRY_FLAG) != 0


def test_opcode_0A_asl_accumulator_updates_zero_flag():
    """Objective: A=0x80 shifts to 0x00 and sets Zero flag."""
    cpu, bus, rom = make_cpu_with_rom()
    rom.write(0x0000, 0x0A)

    cpu.reset()
    cpu.a = 0x80
    cpu.step()

    assert cpu.a == 0x00
    assert (cpu.p & ZERO_FLAG) != 0
    assert (cpu.p & NEGATIVE_FLAG) == 0


def test_opcode_0A_asl_accumulator_updates_negative_flag():
    """Objective: A=0x40 shifts to 0x80 and sets Negative flag."""
    cpu, bus, rom = make_cpu_with_rom()
    rom.write(0x0000, 0x0A)

    cpu.reset()
    cpu.a = 0x40
    cpu.step()

    assert cpu.a == 0x80
    assert (cpu.p & NEGATIVE_FLAG) != 0
    assert (cpu.p & ZERO_FLAG) == 0
