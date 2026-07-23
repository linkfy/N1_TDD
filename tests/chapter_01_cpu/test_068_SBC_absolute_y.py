"""
Add SBC Absolute,Y.

Opcode:
    0xF9 -> SBC $hhhh,Y

Goal:
use absolute_y(cpu), read value, then sbc(cpu, value).
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


def test_sbc_absolute_y_handler_exists_and_is_in_opcode_table():
    """Objective: create sbc_absolute_y(cpu) and add 0xF9 to OPCODE_TABLE."""
    assert hasattr(opcodes, "sbc_absolute_y")
    assert callable(opcodes.sbc_absolute_y)
    assert list(inspect.signature(opcodes.sbc_absolute_y).parameters) == ["cpu"]
    assert opcodes.OPCODE_TABLE[0xF9] is opcodes.sbc_absolute_y


def test_opcode_F9_sbc_absolute_y_subtracts_indexed_value():
    """Objective: F9 00 02 with Y=0x04 subtracts RAM[$0204] from A."""
    cpu, bus, rom = make_cpu_with_rom()
    rom.write(0x0000, 0xF9)
    rom.write(0x0001, 0x00)
    rom.write(0x0002, 0x02)
    bus.write(0x0204, 0x01)

    cpu.reset()
    cpu.a = 0x10
    cpu.y = 0x04
    cpu.flags.set_carry_flag(True)
    cpu.step()

    assert cpu.a == 0x0F
    assert cpu.pc == 0x8003
