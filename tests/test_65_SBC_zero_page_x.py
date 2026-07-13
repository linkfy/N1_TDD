"""
Add SBC Zero Page,X.

Opcode:
    0xF5 -> SBC $nn,X

Goal:
use zero_page_x(cpu), read value, then sbc(cpu, value).
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


def test_sbc_zero_page_x_handler_exists_and_is_in_opcode_table():
    """Objective: create sbc_zero_page_x(cpu) and add 0xF5 to OPCODE_TABLE."""
    assert hasattr(opcodes, "sbc_zero_page_x")
    assert callable(opcodes.sbc_zero_page_x)
    assert list(inspect.signature(opcodes.sbc_zero_page_x).parameters) == ["cpu"]
    assert opcodes.OPCODE_TABLE[0xF5] is opcodes.sbc_zero_page_x


def test_opcode_F5_sbc_zero_page_x_subtracts_indexed_value():
    """Objective: F5 10 with X=0x03 subtracts RAM[$0013] from A."""
    cpu, bus, rom = make_cpu_with_rom()
    rom.write(0x0000, 0xF5)
    rom.write(0x0001, 0x10)
    bus.write(0x0013, 0x01)

    cpu.reset()
    cpu.a = 0x10
    cpu.x = 0x03
    cpu.flags.set_carry_flag(True)
    cpu.step()

    assert cpu.a == 0x0F
    assert cpu.pc == 0x8002


def test_opcode_F5_sbc_zero_page_x_wraps_inside_page_zero():
    """Objective: Zero Page,X wraps before reading the SBC value."""
    cpu, bus, rom = make_cpu_with_rom()
    rom.write(0x0000, 0xF5)
    rom.write(0x0001, 0xFF)
    bus.write(0x0000, 0x01)

    cpu.reset()
    cpu.a = 0x10
    cpu.x = 0x01
    cpu.flags.set_carry_flag(True)
    cpu.step()

    assert cpu.a == 0x0F
    assert cpu.pc == 0x8002
