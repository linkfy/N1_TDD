"""
Add the JMP instruction behavior.

Instruction:
    JMP -> PC = target_address

Goal:
implement jmp(cpu, addr) in instructions.py.

Student guidance:
JMP directly changes the program counter. It does not read memory by itself,
and it does not modify flags.

Important:
PC is a 16-bit register, so keep the assigned address inside 0x0000..0xFFFF:

    cpu.pc = addr & 0xFFFF
"""

from emulator.cpu.instructions import jmp
from tests.helpers import NEGATIVE_FLAG, ZERO_FLAG, make_cpu


CARRY_FLAG = 1 << 0
OVERFLOW_FLAG = 1 << 6


def test_jmp_sets_program_counter_to_target_address():
    """Objective: JMP replaces PC with the target address."""
    cpu = make_cpu()
    cpu.pc = 0x8000

    jmp(cpu, 0x1234)

    assert cpu.pc == 0x1234


def test_jmp_wraps_program_counter_to_16_bits():
    """Objective: PC remains a 16-bit register."""
    cpu = make_cpu()
    cpu.pc = 0x8000

    jmp(cpu, 0x1_0000)

    assert cpu.pc == 0x0000


def test_jmp_does_not_modify_status_flags():
    """Objective: JMP only changes PC; flags are preserved."""
    cpu = make_cpu()
    cpu.p |= CARRY_FLAG
    cpu.p |= ZERO_FLAG
    cpu.p |= OVERFLOW_FLAG
    cpu.p |= NEGATIVE_FLAG

    jmp(cpu, 0x1234)

    assert (cpu.p & CARRY_FLAG) != 0
    assert (cpu.p & ZERO_FLAG) != 0
    assert (cpu.p & OVERFLOW_FLAG) != 0
    assert (cpu.p & NEGATIVE_FLAG) != 0
