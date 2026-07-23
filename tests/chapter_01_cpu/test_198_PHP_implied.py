"""
Add PHP Implied.

Opcode:
    0x08 -> PHP

Goal:
add opcode 0x08 to OPCODE_TABLE.

Student guidance:
PHP uses implied addressing. It has no operand bytes.

The instruction knows what to push from its name:

    PHP -> Push Processor Status

Execution steps:
    1. CPU.step() fetches opcode 0x08.
    2. OPCODE_TABLE dispatches directly to php(cpu).
    3. PHP pushes a status byte with Break set.
    4. PHP decrements S.

Common mistake:
Do not fetch an operand byte for PHP. The byte after opcode 0x08 is the next
instruction, not data used by PHP.
"""
import inspect

from emulator.bus.cpu_bus import CpuBus
from emulator.cpu import opcodes
from emulator.cpu.cpu import CPU
from emulator.cpu.instructions import php
from emulator.memory.fake_rom import FakeROM


CARRY_FLAG = 1 << 0
BREAK_FLAG = 1 << 5
STACK_BASE = 0x0100


def make_cpu_with_rom():
    rom = FakeROM()
    rom.write(0x7FFC, 0x00)
    rom.write(0x7FFD, 0x80)
    bus = CpuBus(program_rom=rom)
    return CPU(bus), bus, rom


def test_php_implied_is_in_opcode_table():
    """Objective: opcode 0x08 is the official PHP opcode."""
    assert opcodes.OPCODE_TABLE[0x08] is php


def test_php_instruction_signature_takes_only_cpu():
    """Objective: PHP is implied, so php(cpu) does not need an operand argument."""
    assert list(inspect.signature(php).parameters) == ["cpu"]


def test_opcode_08_php_pushes_status_to_stack():
    """Objective: executing opcode 0x08 pushes P with Break set."""
    cpu, bus, rom = make_cpu_with_rom()
    rom.write(0x0000, 0x08)

    cpu.reset()
    cpu.p = CARRY_FLAG
    cpu.step()

    pushed_status = bus.read(STACK_BASE | 0xFD)
    assert (pushed_status & CARRY_FLAG) != 0
    assert (pushed_status & BREAK_FLAG) != 0
    assert cpu.s == 0xFC


def test_opcode_08_php_does_not_fetch_operand_bytes():
    """
    Objective:
    PHP is one byte long. The byte after PHP must not be consumed as an operand.

    The pushed value comes from cpu.p, not from program memory after 0x08.
    """
    cpu, bus, rom = make_cpu_with_rom()
    rom.write(0x0000, 0x08)
    rom.write(0x0001, 0x99)

    cpu.reset()
    cpu.p = CARRY_FLAG
    cpu.step()

    pushed_status = bus.read(STACK_BASE | 0xFD)
    assert (pushed_status & CARRY_FLAG) != 0
    assert cpu.pc == 0x8001


def test_opcode_08_php_does_not_leave_break_set_in_cpu_state():
    """
    Objective:
    PHP pushes Break in the saved status byte, but does not keep Break set in
    cpu.p afterward in this emulator model.
    """
    cpu, bus, rom = make_cpu_with_rom()
    rom.write(0x0000, 0x08)

    cpu.reset()
    cpu.p = 0x00
    cpu.step()

    pushed_status = bus.read(STACK_BASE | 0xFD)
    assert (pushed_status & BREAK_FLAG) != 0
    assert cpu.flags.get_break_flag() is False


def test_opcode_08_php_preserves_existing_cpu_flags_except_temporary_break():
    """Objective: PHP should not damage existing CPU status flags."""
    cpu, bus, rom = make_cpu_with_rom()
    rom.write(0x0000, 0x08)

    cpu.reset()
    cpu.p = CARRY_FLAG
    cpu.step()

    assert cpu.p == CARRY_FLAG
