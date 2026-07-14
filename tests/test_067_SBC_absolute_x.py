"""
Add SBC Absolute,X.

Opcode:
    0xFD -> SBC $hhhh,X

Goal:
use absolute_x(cpu), read value, then sbc(cpu, value).
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


def test_sbc_absolute_x_handler_exists_and_is_in_opcode_table():
    """Objective: create sbc_absolute_x(cpu) and add 0xFD to OPCODE_TABLE."""
    assert hasattr(opcodes, "sbc_absolute_x")
    assert callable(opcodes.sbc_absolute_x)
    assert list(inspect.signature(opcodes.sbc_absolute_x).parameters) == ["cpu"]
    assert opcodes.OPCODE_TABLE[0xFD] is opcodes.sbc_absolute_x


def test_opcode_FD_sbc_absolute_x_subtracts_indexed_value():
    """Objective: FD 00 02 with X=0x04 subtracts RAM[$0204] from A."""
    cpu, bus, rom = make_cpu_with_rom()
    rom.write(0x0000, 0xFD)
    rom.write(0x0001, 0x00)
    rom.write(0x0002, 0x02)
    bus.write(0x0204, 0x01)

    cpu.reset()
    cpu.a = 0x10
    cpu.x = 0x04
    cpu.flags.set_carry_flag(True)
    cpu.step()

    assert cpu.a == 0x0F
    assert cpu.pc == 0x8003
