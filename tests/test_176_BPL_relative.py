"""Add BPL Relative: 0x10 -> BPL offset."""
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


def test_bpl_relative_handler_exists_and_is_in_opcode_table():
    """Objective: create bpl_relative(cpu) and add 0x10 to OPCODE_TABLE."""
    assert hasattr(opcodes, "bpl_relative")
    assert callable(opcodes.bpl_relative)
    assert list(inspect.signature(opcodes.bpl_relative).parameters) == ["cpu"]
    assert opcodes.OPCODE_TABLE[0x10] is opcodes.bpl_relative


def test_opcode_10_bpl_relative_branches_when_negative_clear():
    """Objective: BPL branches when Negative is clear."""
    cpu, bus, rom = make_cpu_with_rom()
    rom.write(0x0000, 0x10)
    rom.write(0x0001, 0x05)

    cpu.reset()
    cpu.flags.set_negative_flag(False)
    cpu.step()

    assert cpu.pc == 0x8007


def test_opcode_10_bpl_relative_does_not_branch_when_negative_set():
    """Objective: BPL does not branch when Negative is set."""
    cpu, bus, rom = make_cpu_with_rom()
    rom.write(0x0000, 0x10)
    rom.write(0x0001, 0x05)

    cpu.reset()
    cpu.flags.set_negative_flag(True)
    cpu.step()

    assert cpu.pc == 0x8002
