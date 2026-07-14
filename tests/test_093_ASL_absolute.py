"""
Add ASL Absolute.

Opcode:
    0x0E -> ASL $hhhh

Goal:
create asl_absolute(cpu), use absolute(cpu), then asl(cpu, address).

Student guidance:
Absolute operands are little-endian. For `0E 00 02`, the target address is
$0200, not $0002.
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


def test_asl_absolute_handler_exists_and_is_in_opcode_table():
    """Objective: create asl_absolute(cpu) and add 0x0E to OPCODE_TABLE."""
    assert hasattr(opcodes, "asl_absolute")
    assert callable(opcodes.asl_absolute)
    assert list(inspect.signature(opcodes.asl_absolute).parameters) == ["cpu"]
    assert opcodes.OPCODE_TABLE[0x0E] is opcodes.asl_absolute


def test_opcode_0E_asl_absolute_shifts_memory_value():
    """Objective: 0E 00 02 means ASL $0200, so RAM[$0200] is shifted."""
    cpu, bus, rom = make_cpu_with_rom()
    rom.write(0x0000, 0x0E)
    rom.write(0x0001, 0x00)
    rom.write(0x0002, 0x02)
    bus.write(0x0200, 0b0000_0011)

    cpu.reset()
    cpu.step()

    assert bus.read(0x0200) == 0b0000_0110
    assert cpu.pc == 0x8003
