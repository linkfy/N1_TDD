"""
Add CPY Immediate.

Opcode:
    0xC0 -> CPY #$nn

Goal:
create cpy_immediate(cpu), use immediate(cpu), then cpy(cpu, value).

Student guidance:
Immediate mode returns the compared value directly. CPY does not modify Y.
"""
import inspect

from emulator.bus.cpu_bus import CpuBus
from emulator.cpu import opcodes
from emulator.cpu.cpu import CPU
from emulator.memory.fake_rom import FakeROM
from tests.helpers import NEGATIVE_FLAG, ZERO_FLAG


CARRY_FLAG = 1 << 0


def make_cpu_with_rom():
    rom = FakeROM()
    rom.write(0x7FFC, 0x00)
    rom.write(0x7FFD, 0x80)
    bus = CpuBus(program_rom=rom)
    return CPU(bus), bus, rom


def test_cpy_immediate_handler_exists_and_is_in_opcode_table():
    """Objective: create cpy_immediate(cpu) and add 0xC0 to OPCODE_TABLE."""
    assert hasattr(opcodes, "cpy_immediate")
    assert callable(opcodes.cpy_immediate)
    assert list(inspect.signature(opcodes.cpy_immediate).parameters) == ["cpu"]
    assert opcodes.OPCODE_TABLE[0xC0] is opcodes.cpy_immediate


def test_opcode_C0_cpy_immediate_compares_y_with_value():
    """Objective: C0 10 means compare Y with 0x10."""
    cpu, bus, rom = make_cpu_with_rom()
    rom.write(0x0000, 0xC0)
    rom.write(0x0001, 0x10)

    cpu.reset()
    cpu.y = 0x20
    cpu.step()

    assert cpu.y == 0x20
    assert (cpu.p & CARRY_FLAG) != 0
    assert cpu.pc == 0x8002


def test_opcode_C0_cpy_immediate_sets_zero_when_equal():
    """Objective: equal values set Zero and Carry."""
    cpu, bus, rom = make_cpu_with_rom()
    rom.write(0x0000, 0xC0)
    rom.write(0x0001, 0x10)

    cpu.reset()
    cpu.y = 0x10
    cpu.step()

    assert (cpu.p & ZERO_FLAG) != 0
    assert (cpu.p & CARRY_FLAG) != 0


def test_opcode_C0_cpy_immediate_sets_negative_when_wrapped_result_has_bit_7():
    """Objective: Y=0x01 compared with 0x02 gives wrapped result 0xFF."""
    cpu, bus, rom = make_cpu_with_rom()
    rom.write(0x0000, 0xC0)
    rom.write(0x0001, 0x02)

    cpu.reset()
    cpu.y = 0x01
    cpu.step()

    assert (cpu.p & CARRY_FLAG) == 0
    assert (cpu.p & NEGATIVE_FLAG) != 0
