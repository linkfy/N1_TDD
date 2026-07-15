"""
Add AND (Indirect),Y.

Opcode:
    0x31 -> AND ($nn),Y

Goal:
create and_indirect_y(cpu), use indirect_y(cpu), read memory, then and_a(cpu, value).

Student guidance:
Indirect,Y reads the zero-page pointer first, then adds Y to the final address.
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


def test_and_indirect_y_handler_exists_and_is_in_opcode_table():
    """Objective: create and_indirect_y(cpu) and add 0x31 to OPCODE_TABLE."""
    assert hasattr(opcodes, "and_indirect_y")
    assert callable(opcodes.and_indirect_y)
    assert list(inspect.signature(opcodes.and_indirect_y).parameters) == ["cpu"]
    assert opcodes.OPCODE_TABLE[0x31] is opcodes.and_indirect_y


def test_opcode_31_and_indirect_y_reads_pointed_indexed_memory_value():
    """Objective: 31 20 reads pointer at $20/$21, then adds Y."""
    cpu, bus, rom = make_cpu_with_rom()
    rom.write(0x0000, 0x31)
    rom.write(0x0001, 0x20)
    bus.write(0x0020, 0x00)
    bus.write(0x0021, 0x02)
    bus.write(0x0204, 0x0F)

    cpu.reset()
    cpu.y = 0x04
    cpu.a = 0xF3
    cpu.step()

    assert cpu.a == 0x03
    assert cpu.pc == 0x8002
