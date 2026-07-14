"""
Add SBC (Indirect),Y.

Opcode:
    0xF1 -> SBC ($nn),Y

Goal:
use indirect_y(cpu), read value, then sbc(cpu, value).
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


def test_sbc_indirect_y_handler_exists_and_is_in_opcode_table():
    """Objective: create sbc_indirect_y(cpu) and add 0xF1 to OPCODE_TABLE."""
    assert hasattr(opcodes, "sbc_indirect_y")
    assert callable(opcodes.sbc_indirect_y)
    assert list(inspect.signature(opcodes.sbc_indirect_y).parameters) == ["cpu"]
    assert opcodes.OPCODE_TABLE[0xF1] is opcodes.sbc_indirect_y


def test_opcode_F1_sbc_indirect_y_subtracts_value_from_final_address():
    """Objective: F1 20 with Y=0x04 uses base pointer $0200 and subtracts RAM[$0204]."""
    cpu, bus, rom = make_cpu_with_rom()
    rom.write(0x0000, 0xF1)
    rom.write(0x0001, 0x20)
    bus.write(0x0020, 0x00)
    bus.write(0x0021, 0x02)
    bus.write(0x0204, 0x01)

    cpu.reset()
    cpu.a = 0x10
    cpu.y = 0x04
    cpu.flags.set_carry_flag(True)
    cpu.step()

    assert cpu.a == 0x0F
    assert cpu.pc == 0x8002
