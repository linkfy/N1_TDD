"""
Add EOR Absolute.

Opcode:
    0x4D -> EOR $hhhh

Goal:
create eor_absolute(cpu), use absolute(cpu), read memory, then or_e(cpu, value).

Student guidance:
Absolute operands are little-endian. `4D 00 02` targets $0200.
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


def test_eor_absolute_handler_exists_and_is_in_opcode_table():
    """Objective: create eor_absolute(cpu) and add 0x4D to OPCODE_TABLE."""
    assert hasattr(opcodes, "eor_absolute")
    assert callable(opcodes.eor_absolute)
    assert list(inspect.signature(opcodes.eor_absolute).parameters) == ["cpu"]
    assert opcodes.OPCODE_TABLE[0x4D] is opcodes.eor_absolute


def test_opcode_4D_eor_absolute_reads_memory_value():
    """Objective: 4D 00 02 means EOR value at RAM[$0200]."""
    cpu, bus, rom = make_cpu_with_rom()
    rom.write(0x0000, 0x4D)
    rom.write(0x0001, 0x00)
    rom.write(0x0002, 0x02)
    bus.write(0x0200, 0x0F)

    cpu.reset()
    cpu.a = 0xF0
    cpu.step()

    assert cpu.a == 0xFF
    assert cpu.pc == 0x8003
