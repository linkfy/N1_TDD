"""
Add DEC Zero Page.

Opcode:
    0xC6 -> DEC $nn

Goal:
use zero_page(cpu), then dec(cpu, address).
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


def test_dec_zero_page_handler_exists_and_is_in_opcode_table():
    """Objective: create dec_zero_page(cpu) and add 0xC6 to OPCODE_TABLE."""
    assert hasattr(opcodes, "dec_zero_page")
    assert callable(opcodes.dec_zero_page)
    assert list(inspect.signature(opcodes.dec_zero_page).parameters) == ["cpu"]
    assert opcodes.OPCODE_TABLE[0xC6] is opcodes.dec_zero_page


def test_opcode_C6_dec_zero_page_decrements_memory():
    """Objective: C6 10 means DEC $10, so RAM[$0010] is decremented."""
    cpu, bus, rom = make_cpu_with_rom()
    rom.write(0x0000, 0xC6)
    rom.write(0x0001, 0x10)
    bus.write(0x0010, 0x42)

    cpu.reset()
    cpu.step()

    assert bus.read(0x0010) == 0x41
    assert cpu.pc == 0x8002


def test_opcode_C6_dec_zero_page_updates_zero_flag():
    """Objective: 0x01 - 1 becomes 0x00 and sets Zero flag."""
    cpu, bus, rom = make_cpu_with_rom()
    rom.write(0x0000, 0xC6)
    rom.write(0x0001, 0x10)
    bus.write(0x0010, 0x01)

    cpu.reset()
    cpu.step()

    assert bus.read(0x0010) == 0x00
    assert (cpu.p & ZERO_FLAG) != 0
    assert (cpu.p & NEGATIVE_FLAG) == 0


def test_opcode_C6_dec_zero_page_wraps_to_ff_and_sets_negative_flag():
    """Objective: 0x00 - 1 becomes 0xFF and sets Negative flag."""
    cpu, bus, rom = make_cpu_with_rom()
    rom.write(0x0000, 0xC6)
    rom.write(0x0001, 0x10)
    bus.write(0x0010, 0x00)

    cpu.reset()
    cpu.step()

    assert bus.read(0x0010) == 0xFF
    assert (cpu.p & NEGATIVE_FLAG) != 0
    assert (cpu.p & ZERO_FLAG) == 0
