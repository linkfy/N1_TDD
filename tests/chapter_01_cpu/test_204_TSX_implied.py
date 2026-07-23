"""
Add TSX Implied.

Opcode:
    0xBA -> TSX

Goal:
add opcode 0xBA to OPCODE_TABLE.

Student guidance:
TSX uses implied addressing. It has no operand bytes.

The instruction knows both source and destination from its name:

    TSX -> Transfer Stack Pointer to X

Execution steps:
    1. CPU.step() fetches opcode 0xBA.
    2. OPCODE_TABLE dispatches directly to tsx(cpu).
    3. TSX copies S into X.
    4. TSX updates Zero and Negative flags.

Common mistake:
Do not fetch an operand byte for TSX. The byte after opcode 0xBA is the next
instruction, not data used by TSX.
"""
import inspect

from emulator.bus.cpu_bus import CpuBus
from emulator.cpu import opcodes
from emulator.cpu.cpu import CPU
from emulator.cpu.instructions import tsx
from emulator.memory.fake_rom import FakeROM


def make_cpu_with_rom():
    rom = FakeROM()
    rom.write(0x7FFC, 0x00)
    rom.write(0x7FFD, 0x80)
    bus = CpuBus(program_rom=rom)
    return CPU(bus), bus, rom


def test_tsx_implied_is_in_opcode_table():
    """Objective: opcode 0xBA is the official TSX opcode."""
    assert opcodes.OPCODE_TABLE[0xBA] is tsx


def test_tsx_instruction_signature_takes_only_cpu():
    """Objective: TSX is implied, so tsx(cpu) does not need an operand argument."""
    assert list(inspect.signature(tsx).parameters) == ["cpu"]


def test_opcode_BA_tsx_copies_stack_pointer_to_x():
    """Objective: executing opcode 0xBA copies S into X."""
    cpu, bus, rom = make_cpu_with_rom()
    rom.write(0x0000, 0xBA)

    cpu.reset()
    cpu.s = 0x44
    cpu.x = 0x00
    cpu.step()

    assert cpu.x == 0x44
    assert cpu.s == 0x44


def test_opcode_BA_tsx_updates_zero_and_negative_flags():
    """Objective: TSX opcode behavior includes Zero/Negative flag updates."""
    cpu, bus, rom = make_cpu_with_rom()
    rom.write(0x0000, 0xBA)

    cpu.reset()
    cpu.s = 0x80
    cpu.step()

    assert cpu.x == 0x80
    assert cpu.flags.get_zero_flag() is False
    assert cpu.flags.get_negative_flag() is True


def test_opcode_BA_tsx_does_not_fetch_operand_bytes():
    """
    Objective:
    TSX is one byte long. The byte after TSX must not be consumed as an operand.
    """
    cpu, bus, rom = make_cpu_with_rom()
    rom.write(0x0000, 0xBA)
    rom.write(0x0001, 0x99)

    cpu.reset()
    cpu.s = 0x22
    cpu.step()

    assert cpu.x == 0x22
    assert cpu.pc == 0x8001


def test_opcode_BA_tsx_preserves_flags_other_than_zero_and_negative():
    """Objective: opcode TSX updates only Z/N and preserves unrelated flags."""
    cpu, bus, rom = make_cpu_with_rom()
    rom.write(0x0000, 0xBA)

    cpu.reset()
    cpu.s = 0x01
    cpu.p = 0b1100_0011
    cpu.step()

    assert cpu.x == 0x01
    assert cpu.p & 0b0100_0001 == 0b0100_0001
    assert cpu.flags.get_zero_flag() is False
    assert cpu.flags.get_negative_flag() is False
