"""
Add INC Absolute,X.

Opcode:
    0xFE -> INC $hhhh,X

Goal:
use absolute_x(cpu), then inc(cpu, address).
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


def test_inc_absolute_x_handler_exists_and_is_in_opcode_table():
    """Objective: create inc_absolute_x(cpu) and add 0xFE to OPCODE_TABLE."""
    assert hasattr(opcodes, "inc_absolute_x")
    assert callable(opcodes.inc_absolute_x)
    assert list(inspect.signature(opcodes.inc_absolute_x).parameters) == ["cpu"]
    assert opcodes.OPCODE_TABLE[0xFE] is opcodes.inc_absolute_x


def test_opcode_FE_inc_absolute_x_increments_indexed_memory():
    """Objective: FE 00 02 with X=0x04 increments RAM[$0204]."""
    cpu, bus, rom = make_cpu_with_rom()
    rom.write(0x0000, 0xFE)
    rom.write(0x0001, 0x00)
    rom.write(0x0002, 0x02)
    bus.write(0x0204, 0x41)

    cpu.reset()
    cpu.x = 0x04
    cpu.step()

    assert bus.read(0x0204) == 0x42
    assert cpu.pc == 0x8003
