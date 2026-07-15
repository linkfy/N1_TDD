"""Add BCS Relative: 0xB0 -> BCS offset."""
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


def test_bcs_relative_handler_exists_and_is_in_opcode_table():
    """Objective: create bcs_relative(cpu) and add 0xB0 to OPCODE_TABLE."""
    assert hasattr(opcodes, "bcs_relative")
    assert callable(opcodes.bcs_relative)
    assert list(inspect.signature(opcodes.bcs_relative).parameters) == ["cpu"]
    assert opcodes.OPCODE_TABLE[0xB0] is opcodes.bcs_relative


def test_opcode_B0_bcs_relative_branches_when_carry_set():
    """Objective: BCS branches when Carry is set."""
    cpu, bus, rom = make_cpu_with_rom()
    rom.write(0x0000, 0xB0)
    rom.write(0x0001, 0x05)

    cpu.reset()
    cpu.flags.set_carry_flag(True)
    cpu.step()

    assert cpu.pc == 0x8007


def test_opcode_B0_bcs_relative_does_not_branch_when_carry_clear():
    """Objective: BCS does not branch when Carry is clear."""
    cpu, bus, rom = make_cpu_with_rom()
    rom.write(0x0000, 0xB0)
    rom.write(0x0001, 0x05)

    cpu.reset()
    cpu.flags.set_carry_flag(False)
    cpu.step()

    assert cpu.pc == 0x8002
