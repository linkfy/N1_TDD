"""
Add LDY Immediate.

Opcode:
    0xA0 -> LDY #$nn

Goal:
use immediate(cpu), then ldy(cpu, value).
"""
import inspect

from emulator.bus.cpu_bus import CpuBus
from emulator.cpu import opcodes
from emulator.cpu.cpu import CPU
from emulator.memory.fake_rom import FakeROM
from tests.helpers import NEGATIVE_FLAG, ZERO_FLAG


def make_cpu_with_rom():
    rom = FakeROM()
    rom.write(0x7FFC, 0x00)
    rom.write(0x7FFD, 0x80)
    bus = CpuBus(program_rom=rom)
    return CPU(bus), bus, rom


def test_ldy_immediate_handler_exists_and_is_in_opcode_table():
    """Objective: create ldy_immediate(cpu) and add 0xA0 to OPCODE_TABLE."""
    assert hasattr(opcodes, "ldy_immediate")
    assert callable(opcodes.ldy_immediate)
    assert list(inspect.signature(opcodes.ldy_immediate).parameters) == ["cpu"]
    assert opcodes.OPCODE_TABLE[0xA0] is opcodes.ldy_immediate


def test_opcode_A0_ldy_immediate_loads_register_y():
    """Objective: A0 42 means LDY #$42, so Y becomes 0x42."""
    cpu, _, rom = make_cpu_with_rom()
    rom.write(0x0000, 0xA0)
    rom.write(0x0001, 0x42)

    cpu.reset()
    cpu.step()

    assert cpu.y == 0x42
    assert cpu.pc == 0x8002


def test_opcode_A0_ldy_immediate_updates_flags():
    """Objective: LDY Immediate updates Zero and Negative flags."""
    cpu, _, rom = make_cpu_with_rom()
    rom.write(0x0000, 0xA0)
    rom.write(0x0001, 0x80)

    cpu.reset()
    cpu.step()

    assert cpu.y == 0x80
    assert (cpu.p & ZERO_FLAG) == 0
    assert (cpu.p & NEGATIVE_FLAG) != 0
