"""
Add STA Absolute,Y.

Opcode:
    0x99 -> STA $hhhh,Y

Goal:
use absolute_y(cpu) to get the target address,
then store register A there with sta(cpu, address).
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


def test_sta_absolute_y_handler_exists_and_is_in_opcode_table():
    """
    Objective:
    Create sta_absolute_y(cpu) and add 0x99 to OPCODE_TABLE.
    """
    assert hasattr(opcodes, "sta_absolute_y")
    assert callable(opcodes.sta_absolute_y)
    assert list(inspect.signature(opcodes.sta_absolute_y).parameters) == ["cpu"]
    assert opcodes.OPCODE_TABLE[0x99] is opcodes.sta_absolute_y


def test_opcode_99_sta_absolute_y_stores_register_a():
    """
    Objective:
    99 00 02 means STA $0200,Y.
    If Y is 0x04, store A into RAM $0204.
    """
    cpu, bus, rom = make_cpu_with_rom()
    rom.write(0x0000, 0x99)
    rom.write(0x0001, 0x00)
    rom.write(0x0002, 0x02)

    cpu.reset()
    cpu.a = 0x42
    cpu.y = 0x04
    cpu.step()

    assert bus.read(0x0204) == 0x42
    assert cpu.pc == 0x8003
