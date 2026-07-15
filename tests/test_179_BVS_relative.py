"""Add BVS Relative: 0x70 -> BVS offset."""
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


def test_bvs_relative_handler_exists_and_is_in_opcode_table():
    """Objective: create bvs_relative(cpu) and add 0x70 to OPCODE_TABLE."""
    assert hasattr(opcodes, "bvs_relative")
    assert callable(opcodes.bvs_relative)
    assert list(inspect.signature(opcodes.bvs_relative).parameters) == ["cpu"]
    assert opcodes.OPCODE_TABLE[0x70] is opcodes.bvs_relative


def test_opcode_70_bvs_relative_branches_when_overflow_set():
    """Objective: BVS branches when Overflow is set."""
    cpu, bus, rom = make_cpu_with_rom()
    rom.write(0x0000, 0x70)
    rom.write(0x0001, 0x05)

    cpu.reset()
    cpu.flags.set_overflow_flag(True)
    cpu.step()

    assert cpu.pc == 0x8007


def test_opcode_70_bvs_relative_does_not_branch_when_overflow_clear():
    """Objective: BVS does not branch when Overflow is clear."""
    cpu, bus, rom = make_cpu_with_rom()
    rom.write(0x0000, 0x70)
    rom.write(0x0001, 0x05)

    cpu.reset()
    cpu.flags.set_overflow_flag(False)
    cpu.step()

    assert cpu.pc == 0x8002
