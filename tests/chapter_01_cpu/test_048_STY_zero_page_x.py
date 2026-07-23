"""
Add STY Zero Page,X.

Opcode:
    0x94 -> STY $nn,X

Goal:
use zero_page_x(cpu), then sty(cpu, address).
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


def test_sty_zero_page_x_handler_exists_and_is_in_opcode_table():
    """Objective: create sty_zero_page_x(cpu) and add 0x94 to OPCODE_TABLE."""
    assert hasattr(opcodes, "sty_zero_page_x")
    assert callable(opcodes.sty_zero_page_x)
    assert list(inspect.signature(opcodes.sty_zero_page_x).parameters) == ["cpu"]
    assert opcodes.OPCODE_TABLE[0x94] is opcodes.sty_zero_page_x


def test_opcode_94_sty_zero_page_x_stores_register_y():
    """Objective: 94 10 with X=0x03 stores Y into RAM[$0013]."""
    cpu, bus, rom = make_cpu_with_rom()
    rom.write(0x0000, 0x94)
    rom.write(0x0001, 0x10)

    cpu.reset()
    cpu.y = 0x42
    cpu.x = 0x03
    cpu.step()

    assert bus.read(0x0013) == 0x42
    assert cpu.pc == 0x8002


def test_opcode_94_sty_zero_page_x_wraps():
    """Objective: Zero Page,X wraps inside page $00."""
    cpu, bus, rom = make_cpu_with_rom()
    rom.write(0x0000, 0x94)
    rom.write(0x0001, 0xFF)

    cpu.reset()
    cpu.y = 0x37
    cpu.x = 0x01
    cpu.step()

    assert bus.read(0x0000) == 0x37
    assert cpu.pc == 0x8002
