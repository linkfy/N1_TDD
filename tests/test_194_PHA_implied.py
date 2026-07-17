"""
Add PHA Implied.

Opcode:
    0x48 -> PHA

Goal:
add opcode 0x48 to OPCODE_TABLE.

Student guidance:
PHA uses implied addressing. It has no operand bytes.

The instruction knows what to push from its name:

    PHA -> Push Accumulator

So the opcode handler can dispatch directly to:

    pha(cpu)

Execution steps:
    1. CPU.step() fetches opcode 0x48.
    2. OPCODE_TABLE dispatches to pha(cpu).
    3. PHA writes A to $0100 | S.
    4. PHA decrements S.

Common mistake:
Do not fetch an operand byte for PHA. The byte after opcode 0x48 is the next
instruction, not data used by PHA.
"""
import inspect

from emulator.bus.cpu_bus import CpuBus
from emulator.cpu import opcodes
from emulator.cpu.cpu import CPU
from emulator.cpu.instructions import pha
from emulator.memory.fake_rom import FakeROM


STACK_BASE = 0x0100


def make_cpu_with_rom():
    rom = FakeROM()
    rom.write(0x7FFC, 0x00)
    rom.write(0x7FFD, 0x80)
    bus = CpuBus(program_rom=rom)
    return CPU(bus), bus, rom


def test_pha_implied_is_in_opcode_table():
    """Objective: opcode 0x48 is the official PHA opcode."""
    assert opcodes.OPCODE_TABLE[0x48] is pha


def test_pha_instruction_signature_takes_only_cpu():
    """Objective: PHA is implied, so pha(cpu) does not need an operand argument."""
    assert list(inspect.signature(pha).parameters) == ["cpu"]


def test_opcode_48_pha_pushes_accumulator_to_stack():
    """Objective: executing opcode 0x48 pushes A to the current stack slot."""
    cpu, bus, rom = make_cpu_with_rom()
    rom.write(0x0000, 0x48)

    cpu.reset()
    cpu.a = 0x42
    cpu.step()

    assert bus.read(STACK_BASE | 0xFD) == 0x42
    assert cpu.s == 0xFC


def test_opcode_48_pha_does_not_fetch_operand_bytes():
    """
    Objective:
    PHA is one byte long. The byte after PHA must not be consumed as an operand.

    If the next byte is $99, PHA must ignore it and push A instead.
    """
    cpu, bus, rom = make_cpu_with_rom()
    rom.write(0x0000, 0x48)
    rom.write(0x0001, 0x99)

    cpu.reset()
    cpu.a = 0x55
    cpu.step()

    assert bus.read(STACK_BASE | 0xFD) == 0x55
    assert cpu.pc == 0x8001


def test_opcode_48_pha_does_not_modify_accumulator_or_flags():
    """
    Objective:
    PHA is only a stack push. It does not transform A and it does not update flags.
    """
    cpu, bus, rom = make_cpu_with_rom()
    rom.write(0x0000, 0x48)

    cpu.reset()
    cpu.a = 0x80
    cpu.p = 0x00
    cpu.step()

    assert cpu.a == 0x80
    assert cpu.p == 0x00
    assert bus.read(STACK_BASE | 0xFD) == 0x80
