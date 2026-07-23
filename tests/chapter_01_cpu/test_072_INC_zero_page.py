"""
Add INC Zero Page.

Opcode:
    0xE6 -> INC $nn

Goal:
use zero_page(cpu), then inc(cpu, address).
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


def test_inc_zero_page_handler_exists_and_is_in_opcode_table():
    """Objective: create inc_zero_page(cpu) and add 0xE6 to OPCODE_TABLE."""
    assert hasattr(opcodes, "inc_zero_page")
    assert callable(opcodes.inc_zero_page)
    assert list(inspect.signature(opcodes.inc_zero_page).parameters) == ["cpu"]
    assert opcodes.OPCODE_TABLE[0xE6] is opcodes.inc_zero_page


def test_opcode_E6_inc_zero_page_increments_memory():
    """Objective: E6 10 means INC $10, so RAM[$0010] is incremented."""
    cpu, bus, rom = make_cpu_with_rom()
    rom.write(0x0000, 0xE6)
    rom.write(0x0001, 0x10)
    bus.write(0x0010, 0x41)

    cpu.reset()
    cpu.step()

    assert bus.read(0x0010) == 0x42
    assert cpu.pc == 0x8002


def test_opcode_E6_inc_zero_page_updates_zero_flag():
    """Objective: 0xFF + 1 becomes 0x00 and sets Zero flag."""
    cpu, bus, rom = make_cpu_with_rom()
    rom.write(0x0000, 0xE6)
    rom.write(0x0001, 0x10)
    bus.write(0x0010, 0xFF)

    cpu.reset()
    cpu.step()

    assert bus.read(0x0010) == 0x00
    assert (cpu.p & ZERO_FLAG) != 0
    assert (cpu.p & NEGATIVE_FLAG) == 0


def test_opcode_E6_inc_zero_page_updates_negative_flag():
    """Objective: 0x7F + 1 becomes 0x80 and sets Negative flag."""
    cpu, bus, rom = make_cpu_with_rom()
    rom.write(0x0000, 0xE6)
    rom.write(0x0001, 0x10)
    bus.write(0x0010, 0x7F)

    cpu.reset()
    cpu.step()

    assert bus.read(0x0010) == 0x80
    assert (cpu.p & NEGATIVE_FLAG) != 0
    assert (cpu.p & ZERO_FLAG) == 0
