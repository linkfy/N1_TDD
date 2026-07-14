"""
Add a new instruction: STX.

STX means Store X Register.

Create one function inside emulator/cpu/instructions.py:

    def stx(cpu, address):
        ...

Goal:
write register X into the given memory address.
"""
import inspect

from emulator.cpu import instructions
from tests.helpers import NEGATIVE_FLAG, ZERO_FLAG, make_cpu


def test_stx_instruction_exists():
    """
    Objective:
    Create in instructions.py:
        def stx(cpu, address):
            ...

    Example implementation:
        value = cpu.x
        cpu.bus.write(address, value)

    Important:
    STX receives an address, not a value.
    STX does not update flags.
    """
    assert hasattr(instructions, "stx")
    assert callable(instructions.stx)
    assert list(inspect.signature(instructions.stx).parameters) == ["cpu", "address"]


def test_stx_writes_register_x_to_address():
    """
    Objective:
    stx(cpu, address) must store register X into memory.
    """
    cpu = make_cpu()
    cpu.x = 0x42

    instructions.stx(cpu, 0x0010)

    assert cpu.bus.read(0x0010) == 0x42


def test_stx_does_not_change_zero_or_negative_flags():
    """
    Objective:
    STX must not update Zero or Negative flags.
    """
    cpu = make_cpu()
    cpu.x = 0x00
    cpu.p = NEGATIVE_FLAG

    instructions.stx(cpu, 0x0010)

    assert (cpu.p & ZERO_FLAG) == 0
    assert (cpu.p & NEGATIVE_FLAG) != 0
