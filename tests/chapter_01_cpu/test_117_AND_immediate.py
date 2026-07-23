"""
Add AND Immediate.

Opcode:
    0x29 -> AND #$nn

Goal:
create and_immediate(cpu), use immediate(cpu), then and_a(cpu, value).

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


def test_and_immediate_handler_exists_and_is_in_opcode_table():
    """Objective: create and_immediate(cpu) and add 0x29 to OPCODE_TABLE."""
    assert hasattr(opcodes, "and_immediate")
    assert callable(opcodes.and_immediate)
    assert list(inspect.signature(opcodes.and_immediate).parameters) == ["cpu"]
    assert opcodes.OPCODE_TABLE[0x29] is opcodes.and_immediate


def test_opcode_29_and_immediate_updates_accumulator():
    """Objective: 29 0F means AND #$0F, so A becomes A & 0x0F."""
    cpu, bus, rom = make_cpu_with_rom()
    rom.write(0x0000, 0x29)
    rom.write(0x0001, 0x0F)

    cpu.reset()
    cpu.a = 0xF3
    cpu.step()

    assert cpu.a == 0x03
    assert cpu.pc == 0x8002


def test_opcode_29_and_immediate_updates_zero_flag():
    """Objective: result 0 sets Zero flag."""
    cpu, bus, rom = make_cpu_with_rom()
    rom.write(0x0000, 0x29)
    rom.write(0x0001, 0x0F)

    cpu.reset()
    cpu.a = 0xF0
    cpu.step()

    assert cpu.a == 0x00
    assert (cpu.p & ZERO_FLAG) != 0
    assert (cpu.p & NEGATIVE_FLAG) == 0


def test_opcode_29_and_immediate_updates_negative_flag():
    """Objective: result bit 7 sets Negative flag."""
    cpu, bus, rom = make_cpu_with_rom()
    rom.write(0x0000, 0x29)
    rom.write(0x0001, 0x80)

    cpu.reset()
    cpu.a = 0xFF
    cpu.step()

    assert cpu.a == 0x80
    assert (cpu.p & NEGATIVE_FLAG) != 0
    assert (cpu.p & ZERO_FLAG) == 0
