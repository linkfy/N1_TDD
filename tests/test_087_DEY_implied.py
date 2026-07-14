"""
Add DEY Implied.

Opcode:
    0x88 -> DEY

Goal:
map opcode 0x88 directly to dey(cpu).

Why direct mapping?
DEY uses implied addressing: the operand is implied by the instruction itself.
There is no address or immediate byte to decode.
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


def test_dey_opcode_exists_and_is_in_opcode_table():
    """Objective: add 0x88 to OPCODE_TABLE and point it to dey."""
    assert hasattr(opcodes, "dey")
    assert callable(opcodes.dey)
    assert list(inspect.signature(opcodes.dey).parameters) == ["cpu"]
    assert opcodes.OPCODE_TABLE[0x88] is opcodes.dey


def test_opcode_88_dey_implied_decrements_y_register():
    """Objective: 88 means DEY, so Y is decremented and PC advances by 1."""
    cpu, bus, rom = make_cpu_with_rom()
    rom.write(0x0000, 0x88)

    cpu.reset()
    cpu.y = 0x10
    cpu.step()

    assert cpu.y == 0x0F
    assert cpu.pc == 0x8001


def test_opcode_88_dey_implied_updates_zero_flag():
    """Objective: Y=0x01 becomes 0x00 and sets Zero flag."""
    cpu, bus, rom = make_cpu_with_rom()
    rom.write(0x0000, 0x88)

    cpu.reset()
    cpu.y = 0x01
    cpu.step()

    assert cpu.y == 0x00
    assert (cpu.p & ZERO_FLAG) != 0
    assert (cpu.p & NEGATIVE_FLAG) == 0


def test_opcode_88_dey_implied_updates_negative_flag():
    """Objective: Y=0x00 wraps to 0xFF and sets Negative flag."""
    cpu, bus, rom = make_cpu_with_rom()
    rom.write(0x0000, 0x88)

    cpu.reset()
    cpu.y = 0x00
    cpu.step()

    assert cpu.y == 0xFF
    assert (cpu.p & NEGATIVE_FLAG) != 0
    assert (cpu.p & ZERO_FLAG) == 0
