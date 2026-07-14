"""
Add ADC Zero Page,X.

Opcode:
    0x75 -> ADC $nn,X

Goal:
use zero_page_x(cpu), read value, then adc(cpu, value).
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


def test_adc_zero_page_x_handler_exists_and_is_in_opcode_table():
    """Objective: create adc_zero_page_x(cpu) and add 0x75 to OPCODE_TABLE."""
    assert hasattr(opcodes, "adc_zero_page_x")
    assert callable(opcodes.adc_zero_page_x)
    assert list(inspect.signature(opcodes.adc_zero_page_x).parameters) == ["cpu"]
    assert opcodes.OPCODE_TABLE[0x75] is opcodes.adc_zero_page_x


def test_opcode_75_adc_zero_page_x_adds_indexed_value():
    """Objective: 75 10 with X=0x03 adds RAM[$0013] to A."""
    cpu, bus, rom = make_cpu_with_rom()
    rom.write(0x0000, 0x75)
    rom.write(0x0001, 0x10)
    bus.write(0x0013, 0x05)

    cpu.reset()
    cpu.a = 0x10
    cpu.x = 0x03
    cpu.flags.set_carry_flag(False)
    cpu.step()

    assert cpu.a == 0x15
    assert cpu.pc == 0x8002


def test_opcode_75_adc_zero_page_x_wraps_inside_page_zero():
    """Objective: Zero Page,X wraps before reading the ADC value."""
    cpu, bus, rom = make_cpu_with_rom()
    rom.write(0x0000, 0x75)
    rom.write(0x0001, 0xFF)
    bus.write(0x0000, 0x05)

    cpu.reset()
    cpu.a = 0x10
    cpu.x = 0x01
    cpu.flags.set_carry_flag(False)
    cpu.step()

    assert cpu.a == 0x15
    assert cpu.pc == 0x8002
