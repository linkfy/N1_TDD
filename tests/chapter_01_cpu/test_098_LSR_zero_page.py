"""
Add LSR Zero Page.

Opcode:
    0x46 -> LSR $nn

Goal:
create lsr_zero_page(cpu), use zero_page(cpu), then lsr(cpu, address).

Student guidance:
The operand byte is the zero-page address, not the value to shift. For
`46 10`, read/modify/write RAM[$0010].
"""
import inspect

from emulator.bus.cpu_bus import CpuBus
from emulator.cpu import opcodes
from emulator.cpu.cpu import CPU
from emulator.memory.fake_rom import FakeROM


CARRY_FLAG = 1 << 0


def make_cpu_with_rom():
    rom = FakeROM()
    rom.write(0x7FFC, 0x00)
    rom.write(0x7FFD, 0x80)
    bus = CpuBus(program_rom=rom)
    return CPU(bus), bus, rom


def test_lsr_zero_page_handler_exists_and_is_in_opcode_table():
    """Objective: create lsr_zero_page(cpu) and add 0x46 to OPCODE_TABLE."""
    assert hasattr(opcodes, "lsr_zero_page")
    assert callable(opcodes.lsr_zero_page)
    assert list(inspect.signature(opcodes.lsr_zero_page).parameters) == ["cpu"]
    assert opcodes.OPCODE_TABLE[0x46] is opcodes.lsr_zero_page


def test_opcode_46_lsr_zero_page_shifts_memory_value():
    """Objective: 46 10 means LSR $10, so RAM[$0010] is shifted right."""
    cpu, bus, rom = make_cpu_with_rom()
    rom.write(0x0000, 0x46)
    rom.write(0x0001, 0x10)
    bus.write(0x0010, 0b0000_0110)

    cpu.reset()
    cpu.step()

    assert bus.read(0x0010) == 0b0000_0011
    assert cpu.pc == 0x8002


def test_opcode_46_lsr_zero_page_sets_carry_from_old_bit_0():
    """Objective: old memory bit 0 becomes Carry."""
    cpu, bus, rom = make_cpu_with_rom()
    rom.write(0x0000, 0x46)
    rom.write(0x0001, 0x10)
    bus.write(0x0010, 0b0000_0011)

    cpu.reset()
    cpu.step()

    assert bus.read(0x0010) == 0b0000_0001
    assert (cpu.p & CARRY_FLAG) != 0
