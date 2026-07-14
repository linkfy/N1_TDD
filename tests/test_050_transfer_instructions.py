"""
Add transfer instructions.

These instructions use implied addressing mode.
That means they do not read extra operand bytes.

Instructions:
    TAX -> Transfer A to X
    TXA -> Transfer X to A
    TAY -> Transfer A to Y
    TYA -> Transfer Y to A

Goal:
copy one register into another register and update Zero/Negative flags.
"""
import inspect

from emulator.cpu import instructions
from tests.helpers import NEGATIVE_FLAG, ZERO_FLAG, make_cpu


def test_tax_instruction_exists():
    """
    Objective:
    Create in instructions.py:
        def tax(cpu):
            ...

    TAX means:
        X = A
    """
    assert hasattr(instructions, "tax")
    assert callable(instructions.tax)
    assert list(inspect.signature(instructions.tax).parameters) == ["cpu"]


def test_txa_instruction_exists():
    """
    Objective:
    Create in instructions.py:
        def txa(cpu):
            ...

    TXA means:
        A = X
    """
    assert hasattr(instructions, "txa")
    assert callable(instructions.txa)
    assert list(inspect.signature(instructions.txa).parameters) == ["cpu"]


def test_tay_instruction_exists():
    """
    Objective:
    Create in instructions.py:
        def tay(cpu):
            ...

    TAY means:
        Y = A
    """
    assert hasattr(instructions, "tay")
    assert callable(instructions.tay)
    assert list(inspect.signature(instructions.tay).parameters) == ["cpu"]


def test_tya_instruction_exists():
    """
    Objective:
    Create in instructions.py:
        def tya(cpu):
            ...

    TYA means:
        A = Y
    """
    assert hasattr(instructions, "tya")
    assert callable(instructions.tya)
    assert list(inspect.signature(instructions.tya).parameters) == ["cpu"]


def test_tax_transfers_a_to_x_and_updates_flags():
    """Objective: TAX copies A into X and updates Zero/Negative flags."""
    cpu = make_cpu()
    cpu.a = 0x80

    instructions.tax(cpu)

    assert cpu.x == 0x80
    assert (cpu.p & ZERO_FLAG) == 0
    assert (cpu.p & NEGATIVE_FLAG) != 0


def test_txa_transfers_x_to_a_and_updates_flags():
    """Objective: TXA copies X into A and updates Zero/Negative flags."""
    cpu = make_cpu()
    cpu.x = 0x00

    instructions.txa(cpu)

    assert cpu.a == 0x00
    assert (cpu.p & ZERO_FLAG) != 0
    assert (cpu.p & NEGATIVE_FLAG) == 0


def test_tay_transfers_a_to_y_and_updates_flags():
    """Objective: TAY copies A into Y and updates Zero/Negative flags."""
    cpu = make_cpu()
    cpu.a = 0x42
    cpu.p |= ZERO_FLAG | NEGATIVE_FLAG

    instructions.tay(cpu)

    assert cpu.y == 0x42
    assert (cpu.p & ZERO_FLAG) == 0
    assert (cpu.p & NEGATIVE_FLAG) == 0


def test_tya_transfers_y_to_a_and_updates_flags():
    """Objective: TYA copies Y into A and updates Zero/Negative flags."""
    cpu = make_cpu()
    cpu.y = 0x80

    instructions.tya(cpu)

    assert cpu.a == 0x80
    assert (cpu.p & ZERO_FLAG) == 0
    assert (cpu.p & NEGATIVE_FLAG) != 0
