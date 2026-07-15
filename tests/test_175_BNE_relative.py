"""Add BNE Relative: 0xD0 -> BNE offset."""
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


def test_bne_relative_handler_exists_and_is_in_opcode_table():
    """Objective: create bne_relative(cpu) and add 0xD0 to OPCODE_TABLE."""
    assert hasattr(opcodes, "bne_relative")
    assert callable(opcodes.bne_relative)
    assert list(inspect.signature(opcodes.bne_relative).parameters) == ["cpu"]
    assert opcodes.OPCODE_TABLE[0xD0] is opcodes.bne_relative


def test_opcode_D0_bne_relative_branches_when_zero_clear():
    """Objective: BNE branches when Zero is clear."""
    cpu, bus, rom = make_cpu_with_rom()
    rom.write(0x0000, 0xD0)
    rom.write(0x0001, 0x05)

    cpu.reset()
    cpu.flags.set_zero_flag(False)
    cpu.step()

    assert cpu.pc == 0x8007


def test_opcode_D0_bne_relative_does_not_branch_when_zero_set():
    """Objective: BNE does not branch when Zero is set."""
    cpu, bus, rom = make_cpu_with_rom()
    rom.write(0x0000, 0xD0)
    rom.write(0x0001, 0x05)

    cpu.reset()
    cpu.flags.set_zero_flag(True)
    cpu.step()

    assert cpu.pc == 0x8002
