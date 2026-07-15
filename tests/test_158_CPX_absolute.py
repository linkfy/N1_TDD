"""
Add CPX Absolute.

Opcode:
    0xEC -> CPX $hhhh

Goal:
create cpx_absolute(cpu), use absolute(cpu), read memory, then cpx(cpu, value).

Student guidance:
Absolute operands are little-endian. `EC 00 02` targets $0200.
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


def test_cpx_absolute_handler_exists_and_is_in_opcode_table():
    """Objective: create cpx_absolute(cpu) and add 0xEC to OPCODE_TABLE."""
    assert hasattr(opcodes, "cpx_absolute")
    assert callable(opcodes.cpx_absolute)
    assert list(inspect.signature(opcodes.cpx_absolute).parameters) == ["cpu"]
    assert opcodes.OPCODE_TABLE[0xEC] is opcodes.cpx_absolute


def test_opcode_EC_cpx_absolute_reads_memory_value():
    """Objective: EC 00 02 means compare X with RAM[$0200]."""
    cpu, bus, rom = make_cpu_with_rom()
    rom.write(0x0000, 0xEC)
    rom.write(0x0001, 0x00)
    rom.write(0x0002, 0x02)
    bus.write(0x0200, 0x10)

    cpu.reset()
    cpu.x = 0x20
    cpu.step()

    assert (cpu.p & CARRY_FLAG) != 0
    assert cpu.pc == 0x8003
