"""
Add the NOP instruction behavior.

Instruction:
    NOP -> No Operation

Goal:
implement nop(cpu) in instructions.py.

Student guidance:
NOP intentionally does nothing.

That may feel strange, but it is useful for timing, padding, debugging, and
alignment. In this emulator architecture, CPU.step() already fetches the opcode
and advances PC. Therefore nop(cpu) itself should not change PC or any CPU
state.

Important timeline:
    Before CPU.step():
        PC = $8000

    CPU.step() fetches opcode $EA:
        PC = $8001

    nop(cpu) runs:
        no changes

Common mistakes:
    - Incrementing PC inside nop(cpu).
    - Clearing flags.
    - Treating NOP as an unimplemented opcode error.

Implementation shape:

    def nop(cpu):
        pass
"""

from emulator.cpu.instructions import nop
from tests.helpers import make_cpu


def test_nop_does_not_modify_registers():
    """Objective: NOP does not modify A, X, or Y."""
    cpu = make_cpu()
    cpu.a = 0x11
    cpu.x = 0x22
    cpu.y = 0x33

    nop(cpu)

    assert cpu.a == 0x11
    assert cpu.x == 0x22
    assert cpu.y == 0x33


def test_nop_does_not_modify_stack_pointer():
    """Objective: NOP does not touch S."""
    cpu = make_cpu()
    cpu.s = 0xFD

    nop(cpu)

    assert cpu.s == 0xFD


def test_nop_does_not_modify_program_counter_when_called_directly():
    """
    Objective:
    nop(cpu) itself does not change PC.

    CPU.step() changes PC when it fetches the opcode. The instruction function
    should not add another increment.
    """
    cpu = make_cpu()
    cpu.pc = 0x8001

    nop(cpu)

    assert cpu.pc == 0x8001


def test_nop_does_not_modify_status_flags():
    """Objective: NOP preserves the processor status register P."""
    cpu = make_cpu()
    cpu.p = 0b1100_1111

    nop(cpu)

    assert cpu.p == 0b1100_1111


def test_nop_does_not_modify_memory():
    """Objective: NOP does not read/write data memory as part of instruction logic."""
    cpu = make_cpu()
    cpu.bus.write(0x0002, 0x42)

    nop(cpu)

    assert cpu.bus.read(0x0002) == 0x42
