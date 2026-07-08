"""
Add one more addressing mode: Zero Page,Y.

Create one function inside emulator/cpu/addressing_modes.py:

    def zero_page_y(cpu):
        ...

Goal:
read one byte, add register Y, and keep the result inside page $00.
"""
import inspect

from emulator.bus.cpu_bus import CpuBus
from emulator.cpu import addressing_modes
from emulator.cpu.cpu import CPU
from emulator.memory.fake_rom import FakeROM


def make_cpu_with_rom():
    rom = FakeROM()
    rom.write(0x7FFC, 0x00)
    rom.write(0x7FFD, 0x80)
    bus = CpuBus(program_rom=rom)
    return CPU(bus), bus, rom


def test_zero_page_y_addressing_mode_exists():
    """
    Objective:
    Create in addressing_modes.py:
        def zero_page_y(cpu):
            ...

    Example implementation:
        base = cpu.fetch_byte()
        return (base + cpu.y) & 0xFF
    """
    assert hasattr(addressing_modes, "zero_page_y")
    assert callable(addressing_modes.zero_page_y)
    assert list(inspect.signature(addressing_modes.zero_page_y).parameters) == ["cpu"]


def test_zero_page_y_adds_y_to_base_address():
    """
    Objective:
    If the operand is 0x10 and Y is 0x03,
    zero_page_y(cpu) returns 0x0013.
    """
    cpu, _, rom = make_cpu_with_rom()

    cpu.reset()
    cpu.y = 0x03
    rom.write(0x0000, 0x10)

    addr = addressing_modes.zero_page_y(cpu)

    assert addr == 0x0013
    assert cpu.pc == 0x8001


def test_zero_page_y_wraps_inside_page_zero():
    """
    Objective:
    Zero Page,Y wraps inside page $00.

    Example:
    0xFF + Y=0x01 becomes 0x00, not 0x0100.
    """
    cpu, _, rom = make_cpu_with_rom()

    cpu.reset()
    cpu.y = 0x01
    rom.write(0x0000, 0xFF)

    addr = addressing_modes.zero_page_y(cpu)

    assert addr == 0x0000
    assert cpu.pc == 0x8001
