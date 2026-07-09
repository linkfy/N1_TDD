"""
Add ADC Zero Page.

Opcode:
    0x65 -> ADC $nn

Goal:
use zero_page(cpu), read value, then adc(cpu, value).
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


def test_adc_zero_page_handler_exists_and_is_in_opcode_table():
    """Objective: create adc_zero_page(cpu) and add 0x65 to OPCODE_TABLE."""
    assert hasattr(opcodes, "adc_zero_page")
    assert callable(opcodes.adc_zero_page)
    assert list(inspect.signature(opcodes.adc_zero_page).parameters) == ["cpu"]
    assert opcodes.OPCODE_TABLE[0x65] is opcodes.adc_zero_page


def test_opcode_65_adc_zero_page_adds_value_from_memory():
    """Objective: 65 10 means ADC $10, so add RAM[$0010] to A."""
    cpu, bus, rom = make_cpu_with_rom()
    rom.write(0x0000, 0x65)
    rom.write(0x0001, 0x10)
    bus.write(0x0010, 0x05)

    cpu.reset()
    cpu.a = 0x10
    cpu.flags.set_carry_flag(False)
    cpu.step()

    assert cpu.a == 0x15
    assert cpu.pc == 0x8002
