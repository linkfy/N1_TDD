"""
Add CMP Absolute.

Opcode:
    0xCD -> CMP $hhhh

Goal:
create cmp_absolute(cpu), use absolute(cpu), read memory, then cmp(cpu, value).

Student guidance:
Absolute operands are little-endian. `CD 00 02` targets $0200.
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


def test_cmp_absolute_handler_exists_and_is_in_opcode_table():
    """Objective: create cmp_absolute(cpu) and add 0xCD to OPCODE_TABLE."""
    assert hasattr(opcodes, "cmp_absolute")
    assert callable(opcodes.cmp_absolute)
    assert list(inspect.signature(opcodes.cmp_absolute).parameters) == ["cpu"]
    assert opcodes.OPCODE_TABLE[0xCD] is opcodes.cmp_absolute


def test_opcode_CD_cmp_absolute_reads_memory_value():
    """Objective: CD 00 02 means compare A with RAM[$0200]."""
    cpu, bus, rom = make_cpu_with_rom()
    rom.write(0x0000, 0xCD)
    rom.write(0x0001, 0x00)
    rom.write(0x0002, 0x02)
    bus.write(0x0200, 0x10)

    cpu.reset()
    cpu.a = 0x20
    cpu.step()

    assert (cpu.p & CARRY_FLAG) != 0
    assert cpu.pc == 0x8003
