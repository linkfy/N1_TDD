"""
Add BCC Relative.

Opcode:
    0x90 -> BCC offset

Goal:
create bcc_relative(cpu), use relative(cpu), then bcc(cpu, offset).

Student guidance:
Branch opcodes are two bytes: opcode + signed offset. Even when the branch is
not taken, the offset byte must still be consumed, so PC advances by 2.
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


def test_bcc_relative_handler_exists_and_is_in_opcode_table():
    """Objective: create bcc_relative(cpu) and add 0x90 to OPCODE_TABLE."""
    assert hasattr(opcodes, "bcc_relative")
    assert callable(opcodes.bcc_relative)
    assert list(inspect.signature(opcodes.bcc_relative).parameters) == ["cpu"]
    assert opcodes.OPCODE_TABLE[0x90] is opcodes.bcc_relative


def test_opcode_90_bcc_relative_branches_when_carry_clear():
    """Objective: 90 05 branches from next instruction address 0x8002 to 0x8007."""
    cpu, bus, rom = make_cpu_with_rom()
    rom.write(0x0000, 0x90)
    rom.write(0x0001, 0x05)

    cpu.reset()
    cpu.flags.set_carry_flag(False)
    cpu.step()

    assert cpu.pc == 0x8007


def test_opcode_90_bcc_relative_does_not_branch_when_carry_set():
    """Objective: branch not taken still consumes opcode and offset bytes."""
    cpu, bus, rom = make_cpu_with_rom()
    rom.write(0x0000, 0x90)
    rom.write(0x0001, 0x05)

    cpu.reset()
    cpu.flags.set_carry_flag(True)
    cpu.step()

    assert cpu.pc == 0x8002
