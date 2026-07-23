"""
Add CMP (Indirect),Y.

Opcode:
    0xD1 -> CMP ($nn),Y

Goal:
create cmp_indirect_y(cpu), use indirect_y(cpu), read memory, then cmp(cpu, value).

Student guidance:
Indirect,Y reads the zero-page pointer first, then adds Y to the final address.
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


def test_cmp_indirect_y_handler_exists_and_is_in_opcode_table():
    """Objective: create cmp_indirect_y(cpu) and add 0xD1 to OPCODE_TABLE."""
    assert hasattr(opcodes, "cmp_indirect_y")
    assert callable(opcodes.cmp_indirect_y)
    assert list(inspect.signature(opcodes.cmp_indirect_y).parameters) == ["cpu"]
    assert opcodes.OPCODE_TABLE[0xD1] is opcodes.cmp_indirect_y


def test_opcode_D1_cmp_indirect_y_reads_pointed_indexed_memory_value():
    """Objective: D1 20 reads pointer at $20/$21, then adds Y."""
    cpu, bus, rom = make_cpu_with_rom()
    rom.write(0x0000, 0xD1)
    rom.write(0x0001, 0x20)
    bus.write(0x0020, 0x00)
    bus.write(0x0021, 0x02)
    bus.write(0x0204, 0x10)

    cpu.reset()
    cpu.y = 0x04
    cpu.a = 0x20
    cpu.step()

    assert (cpu.p & CARRY_FLAG) != 0
    assert cpu.pc == 0x8002
