"""
Add ORA Immediate.

Opcode:
    0x09 -> ORA #$nn

Goal:
create ora_immediate(cpu), use immediate(cpu), then or_a(cpu, value).

Student guidance:
Immediate mode returns the operand value directly. Do not read from memory
again for the operand.
"""
import inspect

from emulator.bus.cpu_bus import CpuBus
from emulator.cpu import opcodes
from emulator.cpu.cpu import CPU
from emulator.memory.fake_rom import FakeROM
from tests.helpers import NEGATIVE_FLAG, ZERO_FLAG


def make_cpu_with_rom():
    rom = FakeROM()
    rom.write(0x7FFC, 0x00)
    rom.write(0x7FFD, 0x80)
    bus = CpuBus(program_rom=rom)
    return CPU(bus), bus, rom


def test_ora_immediate_handler_exists_and_is_in_opcode_table():
    """Objective: create ora_immediate(cpu) and add 0x09 to OPCODE_TABLE."""
    assert hasattr(opcodes, "ora_immediate")
    assert callable(opcodes.ora_immediate)
    assert list(inspect.signature(opcodes.ora_immediate).parameters) == ["cpu"]
    assert opcodes.OPCODE_TABLE[0x09] is opcodes.ora_immediate


def test_opcode_09_ora_immediate_updates_accumulator():
    """Objective: 09 0F means ORA #$0F, so A becomes A | 0x0F."""
    cpu, bus, rom = make_cpu_with_rom()
    rom.write(0x0000, 0x09)
    rom.write(0x0001, 0x0F)

    cpu.reset()
    cpu.a = 0xF0
    cpu.step()

    assert cpu.a == 0xFF
    assert cpu.pc == 0x8002


def test_opcode_09_ora_immediate_updates_zero_flag():
    """Objective: result 0 sets Zero flag."""
    cpu, bus, rom = make_cpu_with_rom()
    rom.write(0x0000, 0x09)
    rom.write(0x0001, 0x00)

    cpu.reset()
    cpu.a = 0x00
    cpu.step()

    assert cpu.a == 0x00
    assert (cpu.p & ZERO_FLAG) != 0
    assert (cpu.p & NEGATIVE_FLAG) == 0


def test_opcode_09_ora_immediate_updates_negative_flag():
    """Objective: result bit 7 sets Negative flag."""
    cpu, bus, rom = make_cpu_with_rom()
    rom.write(0x0000, 0x09)
    rom.write(0x0001, 0x80)

    cpu.reset()
    cpu.a = 0x01
    cpu.step()

    assert cpu.a == 0x81
    assert (cpu.p & NEGATIVE_FLAG) != 0
    assert (cpu.p & ZERO_FLAG) == 0
