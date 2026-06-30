"""
Create a method inside cpu called:
    _update_zero_and_negative_flags(self, value) -> None
    This method should delete the repeated code inside our cpu
"""
import pytest

from emulator.bus.cpu_bus import CpuBus
from emulator.cpu.cpu import CPU, NEGATIVE_FLAG, ZERO_FLAG


def make_cpu():
    return CPU(CpuBus())

def test_method_update_zero_and_negative_flags_exists():
    """Optative:
    Declare constants on top of CPU:

    ZERO_FLAG = 1 << 1
    NEGATIVE_FLAG = 1 << 7

    This will help you to have clearest methods

    Objetive:
    Declare in cpu _update_zero_and_negative_flags(self, value: int)
    """
    cpu = make_cpu()

    assert hasattr(cpu, "_update_zero_and_negative_flags")
    assert callable(cpu._update_zero_and_negative_flags)
    
# ---------------------------------------
# Extra tests for check correct behaviour
@pytest.mark.parametrize(
    ("value", "zero_is_set", "negative_is_set"),
    [
        (0x00, True, False),
        (0x01, False, False),
        (0x7F, False, False),
        (0x80, False, True),
        (0xFF, False, True),
    ],
)
def test_update_zero_and_negative_flags_uses_received_value(
    value,
    zero_is_set,
    negative_is_set,
):
    """
    Objective:
    The helper must update Z and N using the received value.

    This protects the refactor: the method should not depend directly on
    cpu.a, because later it can be reused by other registers/instructions.
    """
    cpu = make_cpu()

    cpu.a = 0x00 if value != 0x00 else 0x80
    cpu._update_zero_and_negative_flags(value)

    assert bool(cpu.p & ZERO_FLAG) is zero_is_set
    assert bool(cpu.p & NEGATIVE_FLAG) is negative_is_set


def test_update_zero_and_negative_flags_preserves_other_flags():
    """
    Objective:
    The helper should only modify Zero and Negative flags.

    Other processor status flags must keep their previous value.
    """
    cpu = make_cpu()
    other_flags = 0b0010_1101
    cpu.p = other_flags | ZERO_FLAG | NEGATIVE_FLAG

    cpu._update_zero_and_negative_flags(0x01)

    assert (cpu.p & ZERO_FLAG) == 0
    assert (cpu.p & NEGATIVE_FLAG) == 0
    assert (cpu.p & other_flags) == other_flags
