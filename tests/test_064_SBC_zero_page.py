"""
Add SBC Zero Page.

Opcode:
    0xE5 -> SBC $nn

Goal:
use zero_page(cpu), read value, then sbc(cpu, value).
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


def test_sbc_zero_page_handler_exists_and_is_in_opcode_table():
    """Objective: create sbc_zero_page(cpu) and add 0xE5 to OPCODE_TABLE."""
    assert hasattr(opcodes, "sbc_zero_page")
    assert callable(opcodes.sbc_zero_page)
    assert list(inspect.signature(opcodes.sbc_zero_page).parameters) == ["cpu"]
    assert opcodes.OPCODE_TABLE[0xE5] is opcodes.sbc_zero_page


def test_opcode_E5_sbc_zero_page_subtracts_value_from_memory():
    """Objective: E5 10 means SBC $10, so subtract RAM[$0010] from A."""
    cpu, bus, rom = make_cpu_with_rom()
    rom.write(0x0000, 0xE5)
    rom.write(0x0001, 0x10)
    bus.write(0x0010, 0x01)

    cpu.reset()
    cpu.a = 0x10
    cpu.flags.set_carry_flag(True)
    cpu.step()

    assert cpu.a == 0x0F
    assert cpu.pc == 0x8002
