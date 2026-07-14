"""
Add ADC (Indirect,X).

Opcode:
    0x61 -> ADC ($nn,X)

Goal:
use indirect_x(cpu), read value, then adc(cpu, value).
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


def test_adc_indirect_x_handler_exists_and_is_in_opcode_table():
    """Objective: create adc_indirect_x(cpu) and add 0x61 to OPCODE_TABLE."""
    assert hasattr(opcodes, "adc_indirect_x")
    assert callable(opcodes.adc_indirect_x)
    assert list(inspect.signature(opcodes.adc_indirect_x).parameters) == ["cpu"]
    assert opcodes.OPCODE_TABLE[0x61] is opcodes.adc_indirect_x


def test_opcode_61_adc_indirect_x_adds_value_from_final_address():
    """Objective: 61 20 with X=0x04 uses pointer at $0024 and adds final memory value."""
    cpu, bus, rom = make_cpu_with_rom()
    rom.write(0x0000, 0x61)
    rom.write(0x0001, 0x20)
    bus.write(0x0024, 0x00)
    bus.write(0x0025, 0x02)
    bus.write(0x0200, 0x05)

    cpu.reset()
    cpu.a = 0x10
    cpu.x = 0x04
    cpu.flags.set_carry_flag(False)
    cpu.step()

    assert cpu.a == 0x15
    assert cpu.pc == 0x8002
