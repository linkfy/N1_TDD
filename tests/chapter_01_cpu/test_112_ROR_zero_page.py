"""
Add ROR Zero Page.

Opcode:
    0x66 -> ROR $nn

Goal:
create ror_zero_page(cpu), use zero_page(cpu), then ror(cpu, address).

Student guidance:
The operand byte is the zero-page address, not the value to rotate. For
`66 10`, read/modify/write RAM[$0010].
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


def test_ror_zero_page_handler_exists_and_is_in_opcode_table():
    """Objective: create ror_zero_page(cpu) and add 0x66 to OPCODE_TABLE."""
    assert hasattr(opcodes, "ror_zero_page")
    assert callable(opcodes.ror_zero_page)
    assert list(inspect.signature(opcodes.ror_zero_page).parameters) == ["cpu"]
    assert opcodes.OPCODE_TABLE[0x66] is opcodes.ror_zero_page


def test_opcode_66_ror_zero_page_rotates_memory_value():
    """Objective: 66 10 means ROR $10, so RAM[$0010] is rotated right."""
    cpu, bus, rom = make_cpu_with_rom()
    rom.write(0x0000, 0x66)
    rom.write(0x0001, 0x10)
    bus.write(0x0010, 0b0000_0110)

    cpu.reset()
    cpu.step()

    assert bus.read(0x0010) == 0b0000_0011
    assert cpu.pc == 0x8002


def test_opcode_66_ror_zero_page_uses_old_carry_as_new_bit_7():
    """Objective: old Carry=1 is inserted into memory result bit 7."""
    cpu, bus, rom = make_cpu_with_rom()
    rom.write(0x0000, 0x66)
    rom.write(0x0001, 0x10)
    bus.write(0x0010, 0b0000_0010)

    cpu.reset()
    cpu.p |= CARRY_FLAG
    cpu.step()

    assert bus.read(0x0010) == 0b1000_0001
    assert (cpu.p & CARRY_FLAG) == 0


def test_opcode_66_ror_zero_page_sets_carry_from_old_bit_0():
    """Objective: old memory bit 0 becomes Carry."""
    cpu, bus, rom = make_cpu_with_rom()
    rom.write(0x0000, 0x66)
    rom.write(0x0001, 0x10)
    bus.write(0x0010, 0b0000_0011)

    cpu.reset()
    cpu.step()

    assert bus.read(0x0010) == 0b0000_0001
    assert (cpu.p & CARRY_FLAG) != 0
