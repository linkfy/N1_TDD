"""
Add ROL Absolute,X.

Opcode:
    0x3E -> ROL $hhhh,X

Goal:
create rol_absolute_x(cpu), use absolute_x(cpu), then rol(cpu, address).

Student guidance:
Absolute,X first decodes the 16-bit little-endian base address, then adds X.
For `3E 00 02` with X=0x04, the target address is $0204.
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


def test_rol_absolute_x_handler_exists_and_is_in_opcode_table():
    """Objective: create rol_absolute_x(cpu) and add 0x3E to OPCODE_TABLE."""
    assert hasattr(opcodes, "rol_absolute_x")
    assert callable(opcodes.rol_absolute_x)
    assert list(inspect.signature(opcodes.rol_absolute_x).parameters) == ["cpu"]
    assert opcodes.OPCODE_TABLE[0x3E] is opcodes.rol_absolute_x


def test_opcode_3E_rol_absolute_x_rotates_indexed_memory_value():
    """Objective: 3E 00 02 with X=0x04 rotates RAM[$0204]."""
    cpu, bus, rom = make_cpu_with_rom()
    rom.write(0x0000, 0x3E)
    rom.write(0x0001, 0x00)
    rom.write(0x0002, 0x02)
    bus.write(0x0204, 0b0000_0011)

    cpu.reset()
    cpu.x = 0x04
    cpu.step()

    assert bus.read(0x0204) == 0b0000_0110
    assert cpu.pc == 0x8003
