"""
Add LDY Absolute.

Opcode:
    0xAC -> LDY $hhhh

Goal:
use absolute(cpu), read value, then ldy(cpu, value).
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


def test_ldy_absolute_handler_exists_and_is_in_opcode_table():
    """Objective: create ldy_absolute(cpu) and add 0xAC to OPCODE_TABLE."""
    assert hasattr(opcodes, "ldy_absolute")
    assert callable(opcodes.ldy_absolute)
    assert list(inspect.signature(opcodes.ldy_absolute).parameters) == ["cpu"]
    assert opcodes.OPCODE_TABLE[0xAC] is opcodes.ldy_absolute


def test_opcode_AC_ldy_absolute_loads_register_y():
    """Objective: AC 00 02 means LDY $0200, so Y loads RAM[$0200]."""
    cpu, bus, rom = make_cpu_with_rom()
    rom.write(0x0000, 0xAC)
    rom.write(0x0001, 0x00)
    rom.write(0x0002, 0x02)
    bus.write(0x0200, 0x42)

    cpu.reset()
    cpu.step()

    assert cpu.y == 0x42
    assert cpu.pc == 0x8003
