"""
Add DEC Zero Page,X.

Opcode:
    0xD6 -> DEC $nn,X

Goal:
use zero_page_x(cpu), then dec(cpu, address).
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


def test_dec_zero_page_x_handler_exists_and_is_in_opcode_table():
    """Objective: create dec_zero_page_x(cpu) and add 0xD6 to OPCODE_TABLE."""
    assert hasattr(opcodes, "dec_zero_page_x")
    assert callable(opcodes.dec_zero_page_x)
    assert list(inspect.signature(opcodes.dec_zero_page_x).parameters) == ["cpu"]
    assert opcodes.OPCODE_TABLE[0xD6] is opcodes.dec_zero_page_x


def test_opcode_D6_dec_zero_page_x_decrements_indexed_memory():
    """Objective: D6 10 with X=0x03 decrements RAM[$0013]."""
    cpu, bus, rom = make_cpu_with_rom()
    rom.write(0x0000, 0xD6)
    rom.write(0x0001, 0x10)
    bus.write(0x0013, 0x42)

    cpu.reset()
    cpu.x = 0x03
    cpu.step()

    assert bus.read(0x0013) == 0x41
    assert cpu.pc == 0x8002


def test_opcode_D6_dec_zero_page_x_wraps_inside_page_zero():
    """Objective: Zero Page,X wraps before DEC modifies memory."""
    cpu, bus, rom = make_cpu_with_rom()
    rom.write(0x0000, 0xD6)
    rom.write(0x0001, 0xFF)
    bus.write(0x0000, 0x42)

    cpu.reset()
    cpu.x = 0x01
    cpu.step()

    assert bus.read(0x0000) == 0x41
    assert cpu.pc == 0x8002
