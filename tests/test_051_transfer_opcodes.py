"""
Add transfer opcodes to OPCODE_TABLE.

These opcodes use implied addressing mode.
They do not need opcode handlers because the instruction function already
has the correct shape: def instruction(cpu).

Opcodes:
    0xAA -> TAX
    0x8A -> TXA
    0xA8 -> TAY
    0x98 -> TYA
"""

from emulator.bus.cpu_bus import CpuBus
from emulator.cpu import instructions, opcodes
from emulator.cpu.cpu import CPU
from emulator.memory.fake_rom import FakeROM


def make_cpu_with_rom():
    rom = FakeROM()
    rom.write(0x7FFC, 0x00)
    rom.write(0x7FFD, 0x80)
    bus = CpuBus(program_rom=rom)
    return CPU(bus), bus, rom


def test_transfer_opcodes_are_in_opcode_table():
    """
    Objective:
    Add these entries to OPCODE_TABLE:

        0xAA: tax,
        0x8A: txa,
        0xA8: tay,
        0x98: tya,

    Why:
    These instructions use implied addressing.
    CPU.step() fetches only the opcode, then calls the instruction.
    """
    assert opcodes.OPCODE_TABLE[0xAA] is instructions.tax
    assert opcodes.OPCODE_TABLE[0x8A] is instructions.txa
    assert opcodes.OPCODE_TABLE[0xA8] is instructions.tay
    assert opcodes.OPCODE_TABLE[0x98] is instructions.tya


def test_opcode_AA_tax_transfers_a_to_x():
    """Objective: AA means TAX. It copies A into X."""
    cpu, _, rom = make_cpu_with_rom()
    rom.write(0x0000, 0xAA)

    cpu.reset()
    cpu.a = 0x42
    cpu.step()

    assert cpu.x == 0x42
    assert cpu.pc == 0x8001


def test_opcode_8A_txa_transfers_x_to_a():
    """Objective: 8A means TXA. It copies X into A."""
    cpu, _, rom = make_cpu_with_rom()
    rom.write(0x0000, 0x8A)

    cpu.reset()
    cpu.x = 0x42
    cpu.step()

    assert cpu.a == 0x42
    assert cpu.pc == 0x8001


def test_opcode_A8_tay_transfers_a_to_y():
    """Objective: A8 means TAY. It copies A into Y."""
    cpu, _, rom = make_cpu_with_rom()
    rom.write(0x0000, 0xA8)

    cpu.reset()
    cpu.a = 0x42
    cpu.step()

    assert cpu.y == 0x42
    assert cpu.pc == 0x8001


def test_opcode_98_tya_transfers_y_to_a():
    """Objective: 98 means TYA. It copies Y into A."""
    cpu, _, rom = make_cpu_with_rom()
    rom.write(0x0000, 0x98)

    cpu.reset()
    cpu.y = 0x42
    cpu.step()

    assert cpu.a == 0x42
    assert cpu.pc == 0x8001
