"""
Add DEC Absolute.

Opcode:
    0xCE -> DEC $hhhh

Goal:
use absolute(cpu), then dec(cpu, address).
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


def test_dec_absolute_handler_exists_and_is_in_opcode_table():
    """Objective: create dec_absolute(cpu) and add 0xCE to OPCODE_TABLE."""
    assert hasattr(opcodes, "dec_absolute")
    assert callable(opcodes.dec_absolute)
    assert list(inspect.signature(opcodes.dec_absolute).parameters) == ["cpu"]
    assert opcodes.OPCODE_TABLE[0xCE] is opcodes.dec_absolute


def test_opcode_CE_dec_absolute_decrements_memory():
    """Objective: CE 00 02 means DEC $0200, so RAM[$0200] is decremented."""
    cpu, bus, rom = make_cpu_with_rom()
    rom.write(0x0000, 0xCE)
    rom.write(0x0001, 0x00)
    rom.write(0x0002, 0x02)
    bus.write(0x0200, 0x42)

    cpu.reset()
    cpu.step()

    assert bus.read(0x0200) == 0x41
    assert cpu.pc == 0x8003
