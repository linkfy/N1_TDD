"""
Add STY Zero Page.

Opcode:
    0x84 -> STY $nn

Goal:
use zero_page(cpu), then sty(cpu, address).
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


def test_sty_zero_page_handler_exists_and_is_in_opcode_table():
    """Objective: create sty_zero_page(cpu) and add 0x84 to OPCODE_TABLE."""
    assert hasattr(opcodes, "sty_zero_page")
    assert callable(opcodes.sty_zero_page)
    assert list(inspect.signature(opcodes.sty_zero_page).parameters) == ["cpu"]
    assert opcodes.OPCODE_TABLE[0x84] is opcodes.sty_zero_page


def test_opcode_84_sty_zero_page_stores_register_y():
    """Objective: 84 10 means STY $10, so RAM[$0010] gets Y."""
    cpu, bus, rom = make_cpu_with_rom()
    rom.write(0x0000, 0x84)
    rom.write(0x0001, 0x10)

    cpu.reset()
    cpu.y = 0x42
    cpu.step()

    assert bus.read(0x0010) == 0x42
    assert cpu.pc == 0x8002


def test_opcode_84_sty_zero_page_does_not_change_flags():
    """Objective: STY stores Y but does not update flags."""
    cpu, bus, rom = make_cpu_with_rom()
    rom.write(0x0000, 0x84)
    rom.write(0x0001, 0x10)

    cpu.reset()
    cpu.y = 0x00
    cpu.p = NEGATIVE_FLAG
    cpu.step()

    assert bus.read(0x0010) == 0x00
    assert (cpu.p & ZERO_FLAG) == 0
    assert (cpu.p & NEGATIVE_FLAG) != 0
