"""
Add a new instruction: LDY.

LDY means Load Y Register.

Create one function inside emulator/cpu/instructions.py:

    def ldy(cpu, value):
        ...

Goal:
put value into register Y and update Zero/Negative flags.
"""
import inspect

from emulator.cpu import instructions
from tests.helpers import NEGATIVE_FLAG, ZERO_FLAG, make_cpu


def test_ldy_instruction_exists():
    """
    Objective:
    Create in instructions.py:
        def ldy(cpu, value):
            ...

    Example implementation:
        cpu.y = value
        cpu._update_zero_and_negative_flags(cpu.y)
    """
    assert hasattr(instructions, "ldy")
    assert callable(instructions.ldy)
    assert list(inspect.signature(instructions.ldy).parameters) == ["cpu", "value"]


def test_ldy_loads_value_into_register_y():
    """Objective: ldy(cpu, value) must put value inside cpu.y."""
    cpu = make_cpu()

    instructions.ldy(cpu, 0x42)

    assert cpu.y == 0x42


def test_ldy_sets_zero_flag_when_value_is_zero():
    """Objective: if LDY loads 0x00, Zero flag is set."""
    cpu = make_cpu()

    instructions.ldy(cpu, 0x00)

    assert cpu.y == 0x00
    assert (cpu.p & ZERO_FLAG) != 0


def test_ldy_clears_zero_flag_when_value_is_not_zero():
    """Objective: if LDY loads non-zero value, Zero flag is clear."""
    cpu = make_cpu()
    cpu.p |= ZERO_FLAG

    instructions.ldy(cpu, 0x01)

    assert cpu.y == 0x01
    assert (cpu.p & ZERO_FLAG) == 0


def test_ldy_sets_negative_flag_when_bit_7_is_one():
    """Objective: if LDY loads a value with bit 7 active, Negative flag is set."""
    cpu = make_cpu()

    instructions.ldy(cpu, 0x80)

    assert cpu.y == 0x80
    assert (cpu.p & NEGATIVE_FLAG) != 0


def test_ldy_clears_negative_flag_when_bit_7_is_zero():
    """Objective: if LDY loads a value with bit 7 inactive, Negative flag is clear."""
    cpu = make_cpu()
    cpu.p |= NEGATIVE_FLAG

    instructions.ldy(cpu, 0x7F)

    assert cpu.y == 0x7F
    assert (cpu.p & NEGATIVE_FLAG) == 0
