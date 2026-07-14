"""
Add ASL Zero Page.

Opcode:
    0x06 -> ASL $nn

Goal:
create asl_zero_page(cpu), use zero_page(cpu), then asl(cpu, address).

Student guidance:
The operand byte is not the value to shift. It is the zero-page address where
the value lives. For `06 10`, read/modify/write RAM[$0010].
"""
import inspect

from emulator.bus.cpu_bus import CpuBus
from emulator.cpu import opcodes
from emulator.cpu.cpu import CPU
from emulator.memory.fake_rom import FakeROM
from tests.helpers import NEGATIVE_FLAG, ZERO_FLAG


CARRY_FLAG = 1 << 0


def make_cpu_with_rom():
    rom = FakeROM()
    rom.write(0x7FFC, 0x00)
    rom.write(0x7FFD, 0x80)
    bus = CpuBus(program_rom=rom)
    return CPU(bus), bus, rom


def test_asl_zero_page_handler_exists_and_is_in_opcode_table():
    """Objective: create asl_zero_page(cpu) and add 0x06 to OPCODE_TABLE."""
    assert hasattr(opcodes, "asl_zero_page")
    assert callable(opcodes.asl_zero_page)
    assert list(inspect.signature(opcodes.asl_zero_page).parameters) == ["cpu"]
    assert opcodes.OPCODE_TABLE[0x06] is opcodes.asl_zero_page


def test_opcode_06_asl_zero_page_shifts_memory_value():
    """Objective: 06 10 means ASL $10, so RAM[$0010] is shifted left."""
    cpu, bus, rom = make_cpu_with_rom()
    rom.write(0x0000, 0x06)
    rom.write(0x0001, 0x10)
    bus.write(0x0010, 0b0000_0011)

    cpu.reset()
    cpu.step()

    assert bus.read(0x0010) == 0b0000_0110
    assert cpu.pc == 0x8002


def test_opcode_06_asl_zero_page_sets_carry_from_old_bit_7():
    """Objective: old memory bit 7 becomes Carry."""
    cpu, bus, rom = make_cpu_with_rom()
    rom.write(0x0000, 0x06)
    rom.write(0x0001, 0x10)
    bus.write(0x0010, 0b1000_0001)

    cpu.reset()
    cpu.step()

    assert bus.read(0x0010) == 0b0000_0010
    assert (cpu.p & CARRY_FLAG) != 0


def test_opcode_06_asl_zero_page_updates_zero_flag():
    """Objective: 0x80 shifts to 0x00 and sets Zero flag."""
    cpu, bus, rom = make_cpu_with_rom()
    rom.write(0x0000, 0x06)
    rom.write(0x0001, 0x10)
    bus.write(0x0010, 0x80)

    cpu.reset()
    cpu.step()

    assert bus.read(0x0010) == 0x00
    assert (cpu.p & ZERO_FLAG) != 0
    assert (cpu.p & NEGATIVE_FLAG) == 0


def test_opcode_06_asl_zero_page_updates_negative_flag():
    """Objective: 0x40 shifts to 0x80 and sets Negative flag."""
    cpu, bus, rom = make_cpu_with_rom()
    rom.write(0x0000, 0x06)
    rom.write(0x0001, 0x10)
    bus.write(0x0010, 0x40)

    cpu.reset()
    cpu.step()

    assert bus.read(0x0010) == 0x80
    assert (cpu.p & NEGATIVE_FLAG) != 0
    assert (cpu.p & ZERO_FLAG) == 0
