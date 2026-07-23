"""
Add ADC Immediate.

Opcode:
    0x69 -> ADC #$nn

Goal:
use immediate(cpu), then adc(cpu, value).

Reference:
https://www.nesdev.org/wiki/Instruction_reference#ADC
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


def test_adc_immediate_handler_exists_and_is_in_opcode_table():
    """
    Objective:
    Create adc_immediate(cpu) and add 0x69 to OPCODE_TABLE.

    Important:
    immediate(cpu) returns the value directly.
    Do not read from cpu.bus again for immediate mode.
    """
    assert hasattr(opcodes, "adc_immediate")
    assert callable(opcodes.adc_immediate)
    assert list(inspect.signature(opcodes.adc_immediate).parameters) == ["cpu"]
    assert opcodes.OPCODE_TABLE[0x69] is opcodes.adc_immediate


def test_opcode_69_adc_immediate_adds_value_to_register_a():
    """Objective: 69 05 means ADC #$05, so A = A + 0x05 + Carry."""
    cpu, _, rom = make_cpu_with_rom()
    rom.write(0x0000, 0x69)
    rom.write(0x0001, 0x05)

    cpu.reset()
    cpu.a = 0x10
    cpu.flags.set_carry_flag(False)
    cpu.step()

    assert cpu.a == 0x15
    assert cpu.pc == 0x8002


def test_opcode_69_adc_immediate_uses_carry_flag():
    """Objective: ADC includes the old Carry flag in the addition."""
    cpu, _, rom = make_cpu_with_rom()
    rom.write(0x0000, 0x69)
    rom.write(0x0001, 0x05)

    cpu.reset()
    cpu.a = 0x10
    cpu.flags.set_carry_flag(True)
    cpu.step()

    assert cpu.a == 0x16
    assert cpu.pc == 0x8002
