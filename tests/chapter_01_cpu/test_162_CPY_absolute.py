"""
Add CPY Absolute.

Opcode:
    0xCC -> CPY $hhhh

Goal:
create cpy_absolute(cpu), use absolute(cpu), read memory, then cpy(cpu, value).

Student guidance:
Absolute operands are little-endian. `CC 00 02` targets $0200.
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


def test_cpy_absolute_handler_exists_and_is_in_opcode_table():
    """Objective: create cpy_absolute(cpu) and add 0xCC to OPCODE_TABLE."""
    assert hasattr(opcodes, "cpy_absolute")
    assert callable(opcodes.cpy_absolute)
    assert list(inspect.signature(opcodes.cpy_absolute).parameters) == ["cpu"]
    assert opcodes.OPCODE_TABLE[0xCC] is opcodes.cpy_absolute


def test_opcode_CC_cpy_absolute_reads_memory_value():
    """Objective: CC 00 02 means compare Y with RAM[$0200]."""
    cpu, bus, rom = make_cpu_with_rom()
    rom.write(0x0000, 0xCC)
    rom.write(0x0001, 0x00)
    rom.write(0x0002, 0x02)
    bus.write(0x0200, 0x10)

    cpu.reset()
    cpu.y = 0x20
    cpu.step()

    assert (cpu.p & CARRY_FLAG) != 0
    assert cpu.pc == 0x8003
