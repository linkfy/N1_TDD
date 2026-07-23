"""
Add STA (Indirect),Y.

Opcode:sta_zero_page_x
    0x91 -> STA ($nn),Y

Goal:
use indirect_y(cpu) to get the target address,
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


def test_sta_indirect_y_handler_exists_and_is_in_opcode_table():
    """
    Objective:
    Create sta_indirect_y(cpu) and add 0x91 to OPCODE_TABLE.
    """
    assert hasattr(opcodes, "sta_indirect_y")
    assert callable(opcodes.sta_indirect_y)
    assert list(inspect.signature(opcodes.sta_indirect_y).parameters) == ["cpu"]
    assert opcodes.OPCODE_TABLE[0x91] is opcodes.sta_indirect_y


def test_opcode_91_sta_indirect_y_stores_register_a():
    """
    Objective:
    91 20 means STA ($20),Y.
    If RAM[$0020-$0021] points to $0200 and Y is 0x04,
    store A into RAM $0204.
    """
    cpu, bus, rom = make_cpu_with_rom()
    rom.write(0x0000, 0x91)
    rom.write(0x0001, 0x20)
    bus.write(0x0020, 0x00)
    bus.write(0x0021, 0x02)

    cpu.reset()
    cpu.a = 0x42
    cpu.y = 0x04
    cpu.step()

    assert bus.read(0x0204) == 0x42
    assert cpu.pc == 0x8002
