"""
Add EOR (Indirect,X).

Opcode:
    0x41 -> EOR ($nn,X)

Goal:
create eor_indirect_x(cpu), use indirect_x(cpu), read memory, then or_e(cpu, value).

Student guidance:
Indirect,X adds X to the zero-page operand first, then reads the 16-bit pointer
from zero page.
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


def test_eor_indirect_x_handler_exists_and_is_in_opcode_table():
    """Objective: create eor_indirect_x(cpu) and add 0x41 to OPCODE_TABLE."""
    assert hasattr(opcodes, "eor_indirect_x")
    assert callable(opcodes.eor_indirect_x)
    assert list(inspect.signature(opcodes.eor_indirect_x).parameters) == ["cpu"]
    assert opcodes.OPCODE_TABLE[0x41] is opcodes.eor_indirect_x


def test_opcode_41_eor_indirect_x_reads_pointed_memory_value():
    """Objective: 41 20 with X=0x04 reads pointer at zero-page $24/$25."""
    cpu, bus, rom = make_cpu_with_rom()
    rom.write(0x0000, 0x41)
    rom.write(0x0001, 0x20)
    bus.write(0x0024, 0x00)
    bus.write(0x0025, 0x02)
    bus.write(0x0200, 0x0F)

    cpu.reset()
    cpu.x = 0x04
    cpu.a = 0xF0
    cpu.step()

    assert cpu.a == 0xFF
    assert cpu.pc == 0x8002
