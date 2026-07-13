"""
Add INC Absolute.

Opcode:
    0xEE -> INC $hhhh

Goal:
use absolute(cpu), then inc(cpu, address).
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


def test_inc_absolute_handler_exists_and_is_in_opcode_table():
    """Objective: create inc_absolute(cpu) and add 0xEE to OPCODE_TABLE."""
    assert hasattr(opcodes, "inc_absolute")
    assert callable(opcodes.inc_absolute)
    assert list(inspect.signature(opcodes.inc_absolute).parameters) == ["cpu"]
    assert opcodes.OPCODE_TABLE[0xEE] is opcodes.inc_absolute


def test_opcode_EE_inc_absolute_increments_memory():
    """Objective: EE 00 02 means INC $0200, so RAM[$0200] is incremented."""
    cpu, bus, rom = make_cpu_with_rom()
    rom.write(0x0000, 0xEE)
    rom.write(0x0001, 0x00)
    rom.write(0x0002, 0x02)
    bus.write(0x0200, 0x41)

    cpu.reset()
    cpu.step()

    assert bus.read(0x0200) == 0x42
    assert cpu.pc == 0x8003
