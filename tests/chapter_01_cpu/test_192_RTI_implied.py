"""
Add RTI Implied.

Opcode:
    0x40 -> RTI

Goal:
add opcode 0x40 to OPCODE_TABLE.

Student guidance:
RTI uses implied addressing. It has no operand bytes.

RTI gets all the information it needs from the stack:

    - saved status flags
    - saved PC low byte
    - saved PC high byte

Execution steps:
    1. CPU.step() fetches opcode 0x40.
    2. OPCODE_TABLE dispatches directly to rti(cpu).
    3. RTI pulls status from the stack.
    4. RTI pulls PC low and high from the stack.
    5. PC becomes the exact pulled address.

Important difference from RTS:
    RTS returns to pulled_address + 1.
    RTI returns to pulled_address exactly.

Common mistake:
Do not fetch operand bytes for RTI. It is an implied instruction.
"""
import inspect

from emulator.bus.cpu_bus import CpuBus
from emulator.cpu import opcodes
from emulator.cpu.cpu import CPU
from emulator.cpu.instructions import rti
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


def test_rti_implied_is_in_opcode_table():
    """Objective: opcode 0x40 is the official RTI opcode."""
    assert opcodes.OPCODE_TABLE[0x40] is rti


def test_rti_instruction_signature_takes_only_cpu():
    """Objective: RTI is implied, so rti(cpu) does not need an operand argument."""
    assert list(inspect.signature(rti).parameters) == ["cpu"]


def test_opcode_40_rti_restores_pc_and_status_from_stack():
    """Objective: executing opcode 0x40 restores status and PC from the stack."""
    cpu, bus, rom = make_cpu_with_rom()
    rom.write(0x0000, 0x40)

    cpu.reset()
    cpu.s = 0xFA
    bus.write(STACK_BASE | 0xFB, CARRY_FLAG)
    bus.write(STACK_BASE | 0xFC, 0x34)
    bus.write(STACK_BASE | 0xFD, 0x12)

    cpu.step()

    assert cpu.p == CARRY_FLAG
    assert cpu.pc == 0x1234
    assert cpu.s == 0xFD


def test_opcode_40_rti_does_not_add_one_to_pulled_pc():
    """
    Objective:
    RTI must not behave like RTS.

    If the stack contains PC $8002, RTI returns to $8002 exactly.
    """
    cpu, bus, rom = make_cpu_with_rom()
    rom.write(0x0000, 0x40)

    cpu.reset()
    cpu.s = 0xFA
    bus.write(STACK_BASE | 0xFB, 0x00)
    bus.write(STACK_BASE | 0xFC, 0x02)
    bus.write(STACK_BASE | 0xFD, 0x80)

    cpu.step()

    assert cpu.pc == 0x8002


def test_opcode_40_rti_does_not_fetch_operand_bytes():
    """
    Objective:
    RTI is one byte long. The byte after RTI must not be consumed as an operand.

    The return address comes only from the stack, not from program bytes after
    opcode 0x40.
    """
    cpu, bus, rom = make_cpu_with_rom()
    rom.write(0x0000, 0x40)
    rom.write(0x0001, 0x99)
    rom.write(0x0002, 0x88)

    cpu.reset()
    cpu.s = 0xFA
    bus.write(STACK_BASE | 0xFB, 0x00)
    bus.write(STACK_BASE | 0xFC, 0xCD)
    bus.write(STACK_BASE | 0xFD, 0xAB)

    cpu.step()

    assert cpu.pc == 0xABCD


def test_opcode_40_rti_clears_break_from_restored_cpu_status():
    """
    Objective:
    If the saved status byte has Break set, RTI does not keep Break as a
    persistent CPU status bit in this emulator model.
    """
    cpu, bus, rom = make_cpu_with_rom()
    rom.write(0x0000, 0x40)

    cpu.reset()
    cpu.s = 0xFA
    bus.write(STACK_BASE | 0xFB, BREAK_FLAG | CARRY_FLAG)
    bus.write(STACK_BASE | 0xFC, 0x34)
    bus.write(STACK_BASE | 0xFD, 0x12)

    cpu.step()

    assert cpu.pc == 0x1234
    assert cpu.p == CARRY_FLAG
    assert cpu.flags.get_break_flag() is False
