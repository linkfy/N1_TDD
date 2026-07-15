"""
Add CMP Zero Page,X.

Opcode:
    0xD5 -> CMP $nn,X

Goal:
create cmp_zero_page_x(cpu), use zero_page_x(cpu), read memory, then cmp(cpu, value).

Student guidance:
Zero Page,X wraps inside zero page: (base + X) & 0xFF.
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


def test_cmp_zero_page_x_handler_exists_and_is_in_opcode_table():
    """Objective: create cmp_zero_page_x(cpu) and add 0xD5 to OPCODE_TABLE."""
    assert hasattr(opcodes, "cmp_zero_page_x")
    assert callable(opcodes.cmp_zero_page_x)
    assert list(inspect.signature(opcodes.cmp_zero_page_x).parameters) == ["cpu"]
    assert opcodes.OPCODE_TABLE[0xD5] is opcodes.cmp_zero_page_x


def test_opcode_D5_cmp_zero_page_x_reads_indexed_memory_value():
    """Objective: D5 20 with X=0x04 compares A with RAM[$0024]."""
    cpu, bus, rom = make_cpu_with_rom()
    rom.write(0x0000, 0xD5)
    rom.write(0x0001, 0x20)
    bus.write(0x0024, 0x10)

    cpu.reset()
    cpu.x = 0x04
    cpu.a = 0x20
    cpu.step()

    assert (cpu.p & CARRY_FLAG) != 0
    assert cpu.pc == 0x8002


def test_opcode_D5_cmp_zero_page_x_wraps_zero_page_address():
    """Objective: base=0xFE and X=0x03 reads RAM[$0001]."""
    cpu, bus, rom = make_cpu_with_rom()
    rom.write(0x0000, 0xD5)
    rom.write(0x0001, 0xFE)
    bus.write(0x0001, 0x10)

    cpu.reset()
    cpu.x = 0x03
    cpu.a = 0x20
    cpu.step()

    assert (cpu.p & CARRY_FLAG) != 0
    assert cpu.pc == 0x8002
