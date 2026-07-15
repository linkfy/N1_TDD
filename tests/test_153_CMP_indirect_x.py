"""
Add CMP (Indirect,X).

Opcode:
    0xC1 -> CMP ($nn,X)

Goal:
create cmp_indirect_x(cpu), use indirect_x(cpu), read memory, then cmp(cpu, value).

Student guidance:
Indirect,X adds X to the zero-page operand first, then reads the 16-bit pointer
from zero page.
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


def test_cmp_indirect_x_handler_exists_and_is_in_opcode_table():
    """Objective: create cmp_indirect_x(cpu) and add 0xC1 to OPCODE_TABLE."""
    assert hasattr(opcodes, "cmp_indirect_x")
    assert callable(opcodes.cmp_indirect_x)
    assert list(inspect.signature(opcodes.cmp_indirect_x).parameters) == ["cpu"]
    assert opcodes.OPCODE_TABLE[0xC1] is opcodes.cmp_indirect_x


def test_opcode_C1_cmp_indirect_x_reads_pointed_memory_value():
    """Objective: C1 20 with X=0x04 reads pointer at zero-page $24/$25."""
    cpu, bus, rom = make_cpu_with_rom()
    rom.write(0x0000, 0xC1)
    rom.write(0x0001, 0x20)
    bus.write(0x0024, 0x00)
    bus.write(0x0025, 0x02)
    bus.write(0x0200, 0x10)

    cpu.reset()
    cpu.x = 0x04
    cpu.a = 0x20
    cpu.step()

    assert (cpu.p & CARRY_FLAG) != 0
    assert cpu.pc == 0x8002
