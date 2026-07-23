"""
Add SBC Immediate.

Opcode:
    0xE9 -> SBC #$nn

Goal:
use immediate(cpu), then sbc(cpu, value).

Reference:
https://www.nesdev.org/wiki/Instruction_reference#SBC
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


def test_sbc_immediate_handler_exists_and_is_in_opcode_table():
    """
    Objective:
    Create sbc_immediate(cpu) and add 0xE9 to OPCODE_TABLE.

    Important:
    immediate(cpu) returns the value directly.
    Do not read from cpu.bus again for immediate mode.
    """
    assert hasattr(opcodes, "sbc_immediate")
    assert callable(opcodes.sbc_immediate)
    assert list(inspect.signature(opcodes.sbc_immediate).parameters) == ["cpu"]
    assert opcodes.OPCODE_TABLE[0xE9] is opcodes.sbc_immediate


def test_opcode_E9_sbc_immediate_subtracts_value_from_register_a():
    """
    Objective:
    E9 01 means SBC #$01.

    If Carry is set, A = A - value.
    """
    cpu, _, rom = make_cpu_with_rom()
    rom.write(0x0000, 0xE9)
    rom.write(0x0001, 0x01)

    cpu.reset()
    cpu.a = 0x10
    cpu.flags.set_carry_flag(True)
    cpu.step()

    assert cpu.a == 0x0F
    assert cpu.pc == 0x8002


def test_opcode_E9_sbc_immediate_uses_carry_as_no_borrow():
    """
    Objective:
    If Carry is clear, SBC subtracts one extra.

    A = A - value - 1
    """
    cpu, _, rom = make_cpu_with_rom()
    rom.write(0x0000, 0xE9)
    rom.write(0x0001, 0x01)

    cpu.reset()
    cpu.a = 0x10
    cpu.flags.set_carry_flag(False)
    cpu.step()

    assert cpu.a == 0x0E
    assert cpu.pc == 0x8002
