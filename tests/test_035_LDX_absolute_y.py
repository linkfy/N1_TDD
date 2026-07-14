"""
Add LDX Absolute,Y.

Opcode:
    0xBE -> LDX $hhhh,Y

Goal:
use absolute_y(cpu), read value, then ldx(cpu, value).
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


def test_ldx_absolute_y_handler_exists_and_is_in_opcode_table():
    """Objective: create ldx_absolute_y(cpu) and add 0xBE to OPCODE_TABLE."""
    assert hasattr(opcodes, "ldx_absolute_y")
    assert callable(opcodes.ldx_absolute_y)
    assert list(inspect.signature(opcodes.ldx_absolute_y).parameters) == ["cpu"]
    assert opcodes.OPCODE_TABLE[0xBE] is opcodes.ldx_absolute_y


def test_opcode_BE_ldx_absolute_y_loads_register_x():
    """Objective: BE 00 02 with Y=0x04 reads RAM[$0204] into X."""
    cpu, bus, rom = make_cpu_with_rom()
    rom.write(0x0000, 0xBE)
    rom.write(0x0001, 0x00)
    rom.write(0x0002, 0x02)
    bus.write(0x0204, 0x42)

    cpu.reset()
    cpu.y = 0x04
    cpu.step()

    assert cpu.x == 0x42
    assert cpu.pc == 0x8003
