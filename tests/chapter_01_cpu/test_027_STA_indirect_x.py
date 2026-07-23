"""
Add STA (Indirect,X).

Opcode:
    0x81 -> STA ($nn,X)

Goal:
use indirect_x(cpu) to get the target address,
then store register A there with sta(cpu, address).
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


def test_sta_indirect_x_handler_exists_and_is_in_opcode_table():
    """
    Objective:
    Create sta_indirect_x(cpu) and add 0x81 to OPCODE_TABLE.
    """
    assert hasattr(opcodes, "sta_indirect_x")
    assert callable(opcodes.sta_indirect_x)
    assert list(inspect.signature(opcodes.sta_indirect_x).parameters) == ["cpu"]
    assert opcodes.OPCODE_TABLE[0x81] is opcodes.sta_indirect_x


def test_opcode_81_sta_indirect_x_stores_register_a():
    """
    Objective:
    81 20 means STA ($20,X).
    If X is 0x04, pointer is at $0024.
    If RAM[$0024-$0025] points to $0200, store A into $0200.
    """
    cpu, bus, rom = make_cpu_with_rom()
    rom.write(0x0000, 0x81)
    rom.write(0x0001, 0x20)
    bus.write(0x0024, 0x00)
    bus.write(0x0025, 0x02)

    cpu.reset()
    cpu.a = 0x42
    cpu.x = 0x04
    cpu.step()

    assert bus.read(0x0200) == 0x42
    assert cpu.pc == 0x8002
