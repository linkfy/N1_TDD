"""
Add LDX Zero Page.

Opcode:
    0xA6 -> LDX $nn

Goal:
use zero_page(cpu), read value, then ldx(cpu, value).
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


def test_ldx_zero_page_handler_exists_and_is_in_opcode_table():
    """Objective: create ldx_zero_page(cpu) and add 0xA6 to OPCODE_TABLE."""
    assert hasattr(opcodes, "ldx_zero_page")
    assert callable(opcodes.ldx_zero_page)
    assert list(inspect.signature(opcodes.ldx_zero_page).parameters) == ["cpu"]
    assert opcodes.OPCODE_TABLE[0xA6] is opcodes.ldx_zero_page


def test_opcode_A6_ldx_zero_page_loads_register_x():
    """Objective: A6 10 means LDX $10, so X loads RAM[$0010]."""
    cpu, bus, rom = make_cpu_with_rom()
    rom.write(0x0000, 0xA6)
    rom.write(0x0001, 0x10)
    bus.write(0x0010, 0x42)

    cpu.reset()
    cpu.step()

    assert cpu.x == 0x42
    assert cpu.pc == 0x8002
