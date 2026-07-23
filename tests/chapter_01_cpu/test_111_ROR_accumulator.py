"""
Add ROR Accumulator.

Opcode:
    0x6A -> ROR A

Goal:
map opcode 0x6A directly to ror_a(cpu).

Student guidance:
Accumulator mode has no operand byte. Do not call an addressing helper here.
Opcode 0x6A is one byte long, so PC advances by exactly 1.
"""
import inspect

from emulator.bus.cpu_bus import CpuBus
from emulator.cpu import opcodes
from emulator.cpu.cpu import CPU
from emulator.memory.fake_rom import FakeROM


CARRY_FLAG = 1 << 0


def make_cpu_with_rom():
    rom = FakeROM()
    rom.write(0x7FFC, 0x00)
    rom.write(0x7FFD, 0x80)
    bus = CpuBus(program_rom=rom)
    return CPU(bus), bus, rom


def test_ror_accumulator_opcode_exists_and_is_in_opcode_table():
    """Objective: import ror_a and add 0x6A to OPCODE_TABLE."""
    assert hasattr(opcodes, "ror_a")
    assert callable(opcodes.ror_a)
    assert list(inspect.signature(opcodes.ror_a).parameters) == ["cpu"]
    assert opcodes.OPCODE_TABLE[0x6A] is opcodes.ror_a


def test_opcode_6A_ror_accumulator_rotates_a_and_advances_pc_by_one():
    """Objective: 6A means ROR A, so only A is rotated and PC advances by 1."""
    cpu, bus, rom = make_cpu_with_rom()
    rom.write(0x0000, 0x6A)

    cpu.reset()
    cpu.a = 0b0000_0110
    cpu.step()

    assert cpu.a == 0b0000_0011
    assert cpu.pc == 0x8001


def test_opcode_6A_ror_accumulator_uses_old_carry_as_new_bit_7():
    """Objective: old Carry=1 is inserted into A bit 7."""
    cpu, bus, rom = make_cpu_with_rom()
    rom.write(0x0000, 0x6A)

    cpu.reset()
    cpu.p |= CARRY_FLAG
    cpu.a = 0b0000_0010
    cpu.step()

    assert cpu.a == 0b1000_0001
    assert (cpu.p & CARRY_FLAG) == 0


def test_opcode_6A_ror_accumulator_sets_carry_from_old_a_bit_0():
    """Objective: old A bit 0 becomes Carry."""
    cpu, bus, rom = make_cpu_with_rom()
    rom.write(0x0000, 0x6A)

    cpu.reset()
    cpu.a = 0b0000_0011
    cpu.step()

    assert cpu.a == 0b0000_0001
    assert (cpu.p & CARRY_FLAG) != 0
