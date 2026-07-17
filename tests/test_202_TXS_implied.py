"""
Add TXS Implied.

Opcode:
    0x9A -> TXS

Goal:
add opcode 0x9A to OPCODE_TABLE.

Student guidance:
TXS uses implied addressing. It has no operand bytes.

The instruction knows both source and destination from its name:

    TXS -> Transfer X to Stack Pointer

Execution steps:
    1. CPU.step() fetches opcode 0x9A.
    2. OPCODE_TABLE dispatches directly to txs(cpu).
    3. TXS copies X into S.

Common mistake:
Do not fetch an operand byte for TXS. The byte after opcode 0x9A is the next
instruction, not data used by TXS.
"""
import inspect

from emulator.bus.cpu_bus import CpuBus
from emulator.cpu import opcodes
from emulator.cpu.cpu import CPU
from emulator.cpu.instructions import txs
from emulator.memory.fake_rom import FakeROM


def make_cpu_with_rom():
    rom = FakeROM()
    rom.write(0x7FFC, 0x00)
    rom.write(0x7FFD, 0x80)
    bus = CpuBus(program_rom=rom)
    return CPU(bus), bus, rom


def test_txs_implied_is_in_opcode_table():
    """Objective: opcode 0x9A is the official TXS opcode."""
    assert opcodes.OPCODE_TABLE[0x9A] is txs


def test_txs_instruction_signature_takes_only_cpu():
    """Objective: TXS is implied, so txs(cpu) does not need an operand argument."""
    assert list(inspect.signature(txs).parameters) == ["cpu"]


def test_opcode_9A_txs_copies_x_to_stack_pointer():
    """Objective: executing opcode 0x9A copies X into S."""
    cpu, bus, rom = make_cpu_with_rom()
    rom.write(0x0000, 0x9A)

    cpu.reset()
    cpu.x = 0x44
    cpu.s = 0xFD
    cpu.step()

    assert cpu.s == 0x44
    assert cpu.x == 0x44


def test_opcode_9A_txs_does_not_fetch_operand_bytes():
    """
    Objective:
    TXS is one byte long. The byte after TXS must not be consumed as an operand.
    """
    cpu, bus, rom = make_cpu_with_rom()
    rom.write(0x0000, 0x9A)
    rom.write(0x0001, 0x99)

    cpu.reset()
    cpu.x = 0x22
    cpu.step()

    assert cpu.s == 0x22
    assert cpu.pc == 0x8001


def test_opcode_9A_txs_does_not_update_flags():
    """Objective: opcode TXS preserves status flags."""
    cpu, bus, rom = make_cpu_with_rom()
    rom.write(0x0000, 0x9A)

    cpu.reset()
    cpu.x = 0x00
    cpu.p = 0x00
    cpu.step()

    assert cpu.s == 0x00
    assert cpu.p == 0x00
