"""
Add STY Absolute.

Opcode:
    0x8C -> STY $hhhh

Goal:
use absolute(cpu), then sty(cpu, address).
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


def test_sty_absolute_handler_exists_and_is_in_opcode_table():
    """Objective: create sty_absolute(cpu) and add 0x8C to OPCODE_TABLE."""
    assert hasattr(opcodes, "sty_absolute")
    assert callable(opcodes.sty_absolute)
    assert list(inspect.signature(opcodes.sty_absolute).parameters) == ["cpu"]
    assert opcodes.OPCODE_TABLE[0x8C] is opcodes.sty_absolute


def test_opcode_8C_sty_absolute_stores_register_y():
    """Objective: 8C 00 02 means STY $0200, so RAM[$0200] gets Y."""
    cpu, bus, rom = make_cpu_with_rom()
    rom.write(0x0000, 0x8C)
    rom.write(0x0001, 0x00)
    rom.write(0x0002, 0x02)

    cpu.reset()
    cpu.y = 0x42
    cpu.step()

    assert bus.read(0x0200) == 0x42
    assert cpu.pc == 0x8003


def test_opcode_8C_sty_absolute_does_not_change_flags():
    """Objective: STY Absolute stores Y but does not update flags."""
    cpu, bus, rom = make_cpu_with_rom()
    rom.write(0x0000, 0x8C)
    rom.write(0x0001, 0x00)
    rom.write(0x0002, 0x02)

    cpu.reset()
    cpu.y = 0x00
    cpu.p = NEGATIVE_FLAG
    cpu.step()

    assert bus.read(0x0200) == 0x00
    assert (cpu.p & ZERO_FLAG) == 0
    assert (cpu.p & NEGATIVE_FLAG) != 0
