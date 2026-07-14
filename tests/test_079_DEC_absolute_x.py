"""
Add DEC Absolute,X.

Opcode:
    0xDE -> DEC $hhhh,X

Goal:
use absolute_x(cpu), then dec(cpu, address).
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


def test_dec_absolute_x_handler_exists_and_is_in_opcode_table():
    """Objective: create dec_absolute_x(cpu) and add 0xDE to OPCODE_TABLE."""
    assert hasattr(opcodes, "dec_absolute_x")
    assert callable(opcodes.dec_absolute_x)
    assert list(inspect.signature(opcodes.dec_absolute_x).parameters) == ["cpu"]
    assert opcodes.OPCODE_TABLE[0xDE] is opcodes.dec_absolute_x


def test_opcode_DE_dec_absolute_x_decrements_indexed_memory():
    """Objective: DE 00 02 with X=0x04 decrements RAM[$0204]."""
    cpu, bus, rom = make_cpu_with_rom()
    rom.write(0x0000, 0xDE)
    rom.write(0x0001, 0x00)
    rom.write(0x0002, 0x02)
    bus.write(0x0204, 0x42)

    cpu.reset()
    cpu.x = 0x04
    cpu.step()

    assert bus.read(0x0204) == 0x41
    assert cpu.pc == 0x8003
