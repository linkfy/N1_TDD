"""
Add STX Absolute.

Opcode:
    0x8E -> STX $hhhh

Goal:
use absolute(cpu) to get the target address,
then store register X there with stx(cpu, address).
"""
import inspect

from emulator.bus.cpu_bus import CpuBus
from emulator.cpu import opcodes
from emulator.cpu.cpu import CPU
from emulator.memory.fake_rom import FakeROM
from tests.helpers import NEGATIVE_FLAG, ZERO_FLAG


def make_cpu_with_rom():
    rom = FakeROM()
    rom.write(0x7FFC, 0x00)
    rom.write(0x7FFD, 0x80)
    bus = CpuBus(program_rom=rom)
    return CPU(bus), bus, rom


def test_stx_absolute_handler_exists_and_is_in_opcode_table():
    """
    Objective:
    Create in opcodes.py:
        def stx_absolute(cpu):
            addr = absolute(cpu)
            stx(cpu, addr)

    Then add:
        0x8E: stx_absolute
    """
    assert hasattr(opcodes, "stx_absolute")
    assert callable(opcodes.stx_absolute)
    assert list(inspect.signature(opcodes.stx_absolute).parameters) == ["cpu"]
    assert opcodes.OPCODE_TABLE[0x8E] is opcodes.stx_absolute


def test_opcode_8E_stx_absolute_stores_register_x():
    """
    Objective:
    8E 00 02 means STX $0200.
    Store register X into RAM $0200.
    """
    cpu, bus, rom = make_cpu_with_rom()
    rom.write(0x0000, 0x8E)
    rom.write(0x0001, 0x00)
    rom.write(0x0002, 0x02)

    cpu.reset()
    cpu.x = 0x42
    cpu.step()

    assert bus.read(0x0200) == 0x42
    assert cpu.pc == 0x8003


def test_opcode_8E_stx_absolute_does_not_change_flags():
    """
    Objective:
    STX Absolute stores X but does not update flags.
    """
    cpu, bus, rom = make_cpu_with_rom()
    rom.write(0x0000, 0x8E)
    rom.write(0x0001, 0x00)
    rom.write(0x0002, 0x02)

    cpu.reset()
    cpu.x = 0x00
    cpu.p = NEGATIVE_FLAG
    cpu.step()

    assert bus.read(0x0200) == 0x00
    assert (cpu.p & ZERO_FLAG) == 0
    assert (cpu.p & NEGATIVE_FLAG) != 0
