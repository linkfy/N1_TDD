"""
Add ADC Absolute,X.

Opcode:
    0x7D -> ADC $hhhh,X

Goal:
use absolute_x(cpu), read value, then adc(cpu, value).
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


def test_adc_absolute_x_handler_exists_and_is_in_opcode_table():
    """Objective: create adc_absolute_x(cpu) and add 0x7D to OPCODE_TABLE."""
    assert hasattr(opcodes, "adc_absolute_x")
    assert callable(opcodes.adc_absolute_x)
    assert list(inspect.signature(opcodes.adc_absolute_x).parameters) == ["cpu"]
    assert opcodes.OPCODE_TABLE[0x7D] is opcodes.adc_absolute_x


def test_opcode_7D_adc_absolute_x_adds_indexed_value():
    """Objective: 7D 00 02 with X=0x04 adds RAM[$0204] to A."""
    cpu, bus, rom = make_cpu_with_rom()
    rom.write(0x0000, 0x7D)
    rom.write(0x0001, 0x00)
    rom.write(0x0002, 0x02)
    bus.write(0x0204, 0x05)

    cpu.reset()
    cpu.a = 0x10
    cpu.x = 0x04
    cpu.flags.set_carry_flag(False)
    cpu.step()

    assert cpu.a == 0x15
    assert cpu.pc == 0x8003
