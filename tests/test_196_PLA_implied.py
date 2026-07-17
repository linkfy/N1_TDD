"""
Add PLA Implied.

Opcode:
    0x68 -> PLA

Goal:
add opcode 0x68 to OPCODE_TABLE.

Student guidance:
PLA uses implied addressing. It has no operand bytes.

The instruction knows what to pull from its name:

    PLA -> Pull Accumulator

Execution steps:
    1. CPU.step() fetches opcode 0x68.
    2. OPCODE_TABLE dispatches directly to pla(cpu).
    3. PLA increments S.
    4. PLA reads from $0100 | S.
    5. PLA stores the value in A.
    6. PLA updates Zero and Negative flags.

Common mistake:
Do not fetch an operand byte for PLA. The byte after opcode 0x68 is the next
instruction, not data used by PLA.
"""
import inspect

from emulator.bus.cpu_bus import CpuBus
from emulator.cpu import opcodes
from emulator.cpu.cpu import CPU
from emulator.cpu.instructions import pla
from emulator.memory.fake_rom import FakeROM


STACK_BASE = 0x0100


def make_cpu_with_rom():
    rom = FakeROM()
    rom.write(0x7FFC, 0x00)
    rom.write(0x7FFD, 0x80)
    bus = CpuBus(program_rom=rom)
    return CPU(bus), bus, rom


def test_pla_implied_is_in_opcode_table():
    """Objective: opcode 0x68 is the official PLA opcode."""
    assert opcodes.OPCODE_TABLE[0x68] is pla


def test_pla_instruction_signature_takes_only_cpu():
    """Objective: PLA is implied, so pla(cpu) does not need an operand argument."""
    assert list(inspect.signature(pla).parameters) == ["cpu"]


def test_opcode_68_pla_pulls_stack_value_into_accumulator():
    """Objective: executing opcode 0x68 pulls the next stack byte into A."""
    cpu, bus, rom = make_cpu_with_rom()
    rom.write(0x0000, 0x68)

    cpu.reset()
    cpu.s = 0xFC
    bus.write(STACK_BASE | 0xFD, 0x42)
    cpu.step()

    assert cpu.a == 0x42
    assert cpu.s == 0xFD


def test_opcode_68_pla_updates_zero_and_negative_flags():
    """Objective: PLA opcode behavior includes Zero/Negative flag updates."""
    cpu, bus, rom = make_cpu_with_rom()
    rom.write(0x0000, 0x68)

    cpu.reset()
    cpu.s = 0xFC
    bus.write(STACK_BASE | 0xFD, 0x80)
    cpu.step()

    assert cpu.a == 0x80
    assert cpu.flags.get_zero_flag() is False
    assert cpu.flags.get_negative_flag() is True


def test_opcode_68_pla_does_not_fetch_operand_bytes():
    """
    Objective:
    PLA is one byte long. The byte after PLA must not be consumed as an operand.

    The pulled value comes from the stack, not from program memory after 0x68.
    """
    cpu, bus, rom = make_cpu_with_rom()
    rom.write(0x0000, 0x68)
    rom.write(0x0001, 0x99)

    cpu.reset()
    cpu.s = 0xFC
    bus.write(STACK_BASE | 0xFD, 0x55)
    cpu.step()

    assert cpu.a == 0x55
    assert cpu.pc == 0x8001


def test_opcode_68_pla_preserves_other_flags():
    """Objective: PLA updates Z/N but does not damage unrelated status flags."""
    cpu, bus, rom = make_cpu_with_rom()
    rom.write(0x0000, 0x68)

    cpu.reset()
    cpu.s = 0xFC
    cpu.p = 0b0100_0001
    bus.write(STACK_BASE | 0xFD, 0x01)
    cpu.step()

    assert cpu.a == 0x01
    assert cpu.p & 0b0100_0001 == 0b0100_0001
    assert cpu.flags.get_zero_flag() is False
    assert cpu.flags.get_negative_flag() is False
