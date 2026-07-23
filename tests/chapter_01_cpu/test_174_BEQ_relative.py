"""Add BEQ Relative: 0xF0 -> BEQ offset."""
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


def test_beq_relative_handler_exists_and_is_in_opcode_table():
    """Objective: create beq_relative(cpu) and add 0xF0 to OPCODE_TABLE."""
    assert hasattr(opcodes, "beq_relative")
    assert callable(opcodes.beq_relative)
    assert list(inspect.signature(opcodes.beq_relative).parameters) == ["cpu"]
    assert opcodes.OPCODE_TABLE[0xF0] is opcodes.beq_relative


def test_opcode_F0_beq_relative_branches_when_zero_set():
    """Objective: BEQ branches when Zero is set."""
    cpu, bus, rom = make_cpu_with_rom()
    rom.write(0x0000, 0xF0)
    rom.write(0x0001, 0x05)

    cpu.reset()
    cpu.flags.set_zero_flag(True)
    cpu.step()

    assert cpu.pc == 0x8007


def test_opcode_F0_beq_relative_does_not_branch_when_zero_clear():
    """Objective: BEQ does not branch when Zero is clear."""
    cpu, bus, rom = make_cpu_with_rom()
    rom.write(0x0000, 0xF0)
    rom.write(0x0001, 0x05)

    cpu.reset()
    cpu.flags.set_zero_flag(False)
    cpu.step()

    assert cpu.pc == 0x8002
