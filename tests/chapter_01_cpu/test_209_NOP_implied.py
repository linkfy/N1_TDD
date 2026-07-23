"""
Add NOP Implied.

Opcode:
    0xEA -> NOP

Goal:
add opcode 0xEA to OPCODE_TABLE.

Student guidance:
NOP uses implied addressing. It has no operand bytes.

Execution steps:
    1. CPU.step() fetches opcode 0xEA.
    2. Fetching the opcode increments PC by 1.
    3. OPCODE_TABLE dispatches directly to nop(cpu).
    4. nop(cpu) does nothing.

Therefore, after executing official NOP at $8000:

    PC = $8001

Common mistake:
Do not increment PC inside nop(cpu). CPU.step() already consumed the opcode.
"""
import inspect

from emulator.bus.cpu_bus import CpuBus
from emulator.cpu import opcodes
from emulator.cpu.cpu import CPU
from emulator.cpu.instructions import nop
from emulator.memory.fake_rom import FakeROM


def make_cpu_with_rom():
    rom = FakeROM()
    rom.write(0x7FFC, 0x00)
    rom.write(0x7FFD, 0x80)
    bus = CpuBus(program_rom=rom)
    return CPU(bus), bus, rom


def test_nop_implied_is_in_opcode_table():
    """Objective: opcode 0xEA is the official NOP opcode."""
    assert opcodes.OPCODE_TABLE[0xEA] is nop


def test_nop_instruction_signature_takes_only_cpu():
    """Objective: NOP is implied, so nop(cpu) does not need an operand argument."""
    assert list(inspect.signature(nop).parameters) == ["cpu"]


def test_opcode_EA_nop_advances_pc_only_by_opcode_fetch():
    """
    Objective:
    Executing opcode 0xEA advances PC from $8000 to $8001.

    That one-byte advance comes from CPU.step() fetching the opcode, not from
    nop(cpu) itself.
    """
    cpu, bus, rom = make_cpu_with_rom()
    rom.write(0x0000, 0xEA)

    cpu.reset()
    cpu.step()

    assert cpu.pc == 0x8001


def test_opcode_EA_nop_does_not_fetch_operand_bytes():
    """
    Objective:
    NOP is one byte long. The byte after NOP is the next instruction, not an
    operand consumed by NOP.
    """
    cpu, bus, rom = make_cpu_with_rom()
    rom.write(0x0000, 0xEA)
    rom.write(0x0001, 0x99)

    cpu.reset()
    cpu.step()

    assert cpu.pc == 0x8001


def test_opcode_EA_nop_preserves_registers_and_flags():
    """Objective: executing NOP preserves registers and flags."""
    cpu, bus, rom = make_cpu_with_rom()
    rom.write(0x0000, 0xEA)

    cpu.reset()
    cpu.a = 0x11
    cpu.x = 0x22
    cpu.y = 0x33
    cpu.s = 0xFD
    cpu.p = 0b1100_1111
    cpu.step()

    assert cpu.a == 0x11
    assert cpu.x == 0x22
    assert cpu.y == 0x33
    assert cpu.s == 0xFD
    assert cpu.p == 0b1100_1111
