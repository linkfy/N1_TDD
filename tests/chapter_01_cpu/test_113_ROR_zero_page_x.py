"""
Add ROR Zero Page,X.

Opcode:
    0x76 -> ROR $nn,X

Goal:
create ror_zero_page_x(cpu), use zero_page_x(cpu), then ror(cpu, address).

Student guidance:
Zero Page,X wraps inside the zero page. For base=0xFE and X=0x03, the final
address is (0xFE + 0x03) & 0xFF == 0x01.
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


def test_ror_zero_page_x_handler_exists_and_is_in_opcode_table():
    """Objective: create ror_zero_page_x(cpu) and add 0x76 to OPCODE_TABLE."""
    assert hasattr(opcodes, "ror_zero_page_x")
    assert callable(opcodes.ror_zero_page_x)
    assert list(inspect.signature(opcodes.ror_zero_page_x).parameters) == ["cpu"]
    assert opcodes.OPCODE_TABLE[0x76] is opcodes.ror_zero_page_x


def test_opcode_76_ror_zero_page_x_rotates_indexed_memory_value():
    """Objective: 76 20 with X=0x04 rotates RAM[$0024]."""
    cpu, bus, rom = make_cpu_with_rom()
    rom.write(0x0000, 0x76)
    rom.write(0x0001, 0x20)
    bus.write(0x0024, 0b0000_0110)

    cpu.reset()
    cpu.x = 0x04
    cpu.step()

    assert bus.read(0x0024) == 0b0000_0011
    assert cpu.pc == 0x8002


def test_opcode_76_ror_zero_page_x_wraps_zero_page_address():
    """Objective: zero-page indexed addresses wrap to 8 bits."""
    cpu, bus, rom = make_cpu_with_rom()
    rom.write(0x0000, 0x76)
    rom.write(0x0001, 0xFE)
    bus.write(0x0001, 0x04)

    cpu.reset()
    cpu.x = 0x03
    cpu.step()

    assert bus.read(0x0001) == 0x02
    assert cpu.pc == 0x8002
