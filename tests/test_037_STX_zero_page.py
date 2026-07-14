"""
Add STX Zero Page.

Opcode:
    0x86 -> STX $nn

Goal:
use zero_page(cpu) to get the target address,
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


def test_stx_zero_page_handler_exists_and_is_in_opcode_table():
    """
    Objective:
    Create in opcodes.py:
        def stx_zero_page(cpu):
            addr = zero_page(cpu)
            stx(cpu, addr)

    Then add:
        0x86: stx_zero_page
    """
    assert hasattr(opcodes, "stx_zero_page")
    assert callable(opcodes.stx_zero_page)
    assert list(inspect.signature(opcodes.stx_zero_page).parameters) == ["cpu"]
    assert opcodes.OPCODE_TABLE[0x86] is opcodes.stx_zero_page


def test_opcode_86_stx_zero_page_stores_register_x():
    """
    Objective:
    86 10 means STX $10.
    Store register X into RAM $0010.
    """
    cpu, bus, rom = make_cpu_with_rom()
    rom.write(0x0000, 0x86)
    rom.write(0x0001, 0x10)

    cpu.reset()
    cpu.x = 0x42
    cpu.step()

    assert bus.read(0x0010) == 0x42
    assert cpu.pc == 0x8002


def test_opcode_86_stx_zero_page_does_not_change_flags():
    """
    Objective:
    STX Zero Page stores X but does not update flags.
    """
    cpu, bus, rom = make_cpu_with_rom()
    rom.write(0x0000, 0x86)
    rom.write(0x0001, 0x10)

    cpu.reset()
    cpu.x = 0x00
    cpu.p = NEGATIVE_FLAG
    cpu.step()

    assert bus.read(0x0010) == 0x00
    assert (cpu.p & ZERO_FLAG) == 0
    assert (cpu.p & NEGATIVE_FLAG) != 0
