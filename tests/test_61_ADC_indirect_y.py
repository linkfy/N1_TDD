"""
Add ADC (Indirect),Y.

Opcode:
    0x71 -> ADC ($nn),Y

Goal:
use indirect_y(cpu), read value, then adc(cpu, value).
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


def test_adc_indirect_y_handler_exists_and_is_in_opcode_table():
    """Objective: create adc_indirect_y(cpu) and add 0x71 to OPCODE_TABLE."""
    assert hasattr(opcodes, "adc_indirect_y")
    assert callable(opcodes.adc_indirect_y)
    assert list(inspect.signature(opcodes.adc_indirect_y).parameters) == ["cpu"]
    assert opcodes.OPCODE_TABLE[0x71] is opcodes.adc_indirect_y


def test_opcode_71_adc_indirect_y_adds_value_from_final_address():
    """Objective: 71 20 with Y=0x04 uses base pointer $0200 and adds RAM[$0204]."""
    cpu, bus, rom = make_cpu_with_rom()
    rom.write(0x0000, 0x71)
    rom.write(0x0001, 0x20)
    bus.write(0x0020, 0x00)
    bus.write(0x0021, 0x02)
    bus.write(0x0204, 0x05)

    cpu.reset()
    cpu.a = 0x10
    cpu.y = 0x04
    cpu.flags.set_carry_flag(False)
    cpu.step()

    assert cpu.a == 0x15
    assert cpu.pc == 0x8002
