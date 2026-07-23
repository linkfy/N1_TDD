"""
Add JSR Absolute.

Opcode:
    0x20 -> JSR $hhhh

Goal:
create jsr_absolute(cpu), use absolute(cpu), then jsr(cpu, addr).

Student guidance:
JSR absolute uses a 16-bit little-endian operand as the subroutine address.

Example:
    20 34 12 -> JSR $1234

Execution steps:
    1. CPU.step() fetches opcode 0x20.
    2. absolute(cpu) fetches operand bytes 34 12 and returns $1234.
    3. PC now points to the next instruction, $8003 in these tests.
    4. jsr(cpu, $1234) pushes return address $8002.
    5. PC becomes $1234.

Common mistake:
Do not call jmp(cpu, addr). JSR must push the return address first.
"""
import inspect

from emulator.bus.cpu_bus import CpuBus
from emulator.cpu import opcodes
from emulator.cpu.cpu import CPU
from emulator.memory.fake_rom import FakeROM


STACK_BASE = 0x0100


def make_cpu_with_rom():
    rom = FakeROM()
    rom.write(0x7FFC, 0x00)
    rom.write(0x7FFD, 0x80)
    bus = CpuBus(program_rom=rom)
    return CPU(bus), bus, rom


def test_jsr_absolute_handler_exists_and_is_in_opcode_table():
    """Objective: create jsr_absolute(cpu) and add 0x20 to OPCODE_TABLE."""
    assert hasattr(opcodes, "jsr_absolute")
    assert callable(opcodes.jsr_absolute)
    assert list(inspect.signature(opcodes.jsr_absolute).parameters) == ["cpu"]
    assert opcodes.OPCODE_TABLE[0x20] is opcodes.jsr_absolute


def test_opcode_20_jsr_absolute_jumps_to_subroutine_address():
    """Objective: 20 34 12 means JSR $1234, so PC becomes $1234."""
    cpu, bus, rom = make_cpu_with_rom()
    rom.write(0x0000, 0x20)
    rom.write(0x0001, 0x34)
    rom.write(0x0002, 0x12)

    cpu.reset()
    cpu.step()

    assert cpu.pc == 0x1234


def test_opcode_20_jsr_absolute_pushes_return_address_to_stack():
    """
    Objective:
    After fetching opcode + 2-byte operand, PC is $8003.
    JSR pushes $8002, high byte first, low byte second.
    """
    cpu, bus, rom = make_cpu_with_rom()
    rom.write(0x0000, 0x20)
    rom.write(0x0001, 0x34)
    rom.write(0x0002, 0x12)

    cpu.reset()
    cpu.step()

    assert bus.read(STACK_BASE | 0xFD) == 0x80
    assert bus.read(STACK_BASE | 0xFC) == 0x02
    assert cpu.s == 0xFB


def test_opcode_20_jsr_absolute_does_not_behave_like_jmp():
    """
    Objective:
    JSR must save a return address. If jsr_absolute accidentally calls jmp,
    PC may be correct, but the stack will not contain the return address.
    """
    cpu, bus, rom = make_cpu_with_rom()
    rom.write(0x0000, 0x20)
    rom.write(0x0001, 0x34)
    rom.write(0x0002, 0x12)

    cpu.reset()
    cpu.step()

    assert cpu.pc == 0x1234
    assert bus.read(STACK_BASE | 0xFD) == 0x80
    assert bus.read(STACK_BASE | 0xFC) == 0x02
