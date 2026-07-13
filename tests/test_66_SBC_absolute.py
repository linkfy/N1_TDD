"""
Add SBC Absolute.

Opcode:
    0xED -> SBC $hhhh

Goal:
use absolute(cpu), read value, then sbc(cpu, value).
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


def test_sbc_absolute_handler_exists_and_is_in_opcode_table():
    """Objective: create sbc_absolute(cpu) and add 0xED to OPCODE_TABLE."""
    assert hasattr(opcodes, "sbc_absolute")
    assert callable(opcodes.sbc_absolute)
    assert list(inspect.signature(opcodes.sbc_absolute).parameters) == ["cpu"]
    assert opcodes.OPCODE_TABLE[0xED] is opcodes.sbc_absolute


def test_opcode_ED_sbc_absolute_subtracts_value_from_memory():
    """Objective: ED 00 02 means SBC $0200, so subtract RAM[$0200] from A."""
    cpu, bus, rom = make_cpu_with_rom()
    rom.write(0x0000, 0xED)
    rom.write(0x0001, 0x00)
    rom.write(0x0002, 0x02)
    bus.write(0x0200, 0x01)

    cpu.reset()
    cpu.a = 0x10
    cpu.flags.set_carry_flag(True)
    cpu.step()

    assert cpu.a == 0x0F
    assert cpu.pc == 0x8003
