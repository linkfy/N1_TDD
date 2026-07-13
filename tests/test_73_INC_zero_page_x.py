"""
Add INC Zero Page,X.

Opcode:
    0xF6 -> INC $nn,X

Goal:
use zero_page_x(cpu), then inc(cpu, address).
"""
import inspect

from emulator.bus.cpu_bus import CpuBus
from emulator.cpu import opcodes
from emulator.cpu.cpu import CPU
from emulator.memory.fake_rom import FakeROM


def make_cpu_with_rom():
    rom = FakeROM()
    rom.write(0x7FFC, 0x00)
    rom.write(0x7FFD, 0x80)
    bus = CpuBus(program_rom=rom)
    return CPU(bus), bus, rom


def test_inc_zero_page_x_handler_exists_and_is_in_opcode_table():
    """Objective: create inc_zero_page_x(cpu) and add 0xF6 to OPCODE_TABLE."""
    assert hasattr(opcodes, "inc_zero_page_x")
    assert callable(opcodes.inc_zero_page_x)
    assert list(inspect.signature(opcodes.inc_zero_page_x).parameters) == ["cpu"]
    assert opcodes.OPCODE_TABLE[0xF6] is opcodes.inc_zero_page_x


def test_opcode_F6_inc_zero_page_x_increments_indexed_memory():
    """Objective: F6 10 with X=0x03 increments RAM[$0013]."""
    cpu, bus, rom = make_cpu_with_rom()
    rom.write(0x0000, 0xF6)
    rom.write(0x0001, 0x10)
    bus.write(0x0013, 0x41)

    cpu.reset()
    cpu.x = 0x03
    cpu.step()

    assert bus.read(0x0013) == 0x42
    assert cpu.pc == 0x8002


def test_opcode_F6_inc_zero_page_x_wraps_inside_page_zero():
    """Objective: Zero Page,X wraps before INC modifies memory."""
    cpu, bus, rom = make_cpu_with_rom()
    rom.write(0x0000, 0xF6)
    rom.write(0x0001, 0xFF)
    bus.write(0x0000, 0x41)

    cpu.reset()
    cpu.x = 0x01
    cpu.step()

    assert bus.read(0x0000) == 0x42
    assert cpu.pc == 0x8002
