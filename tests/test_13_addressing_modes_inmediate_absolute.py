"""
Refactor the addressing code we already have in CPU.step().

Create two functions inside emulator/cpu/addressing_modes.py:

    def immediate(cpu):
        ...

    def absolute(cpu):
        ...

The goal is simple:
move the code that gets values or addresses out of CPU.step().
This will make CPU.step() smaller and easier to read.
"""
import inspect
from pathlib import Path

from emulator.cpu import addressing_modes
from tests.helpers import make_cpu


def test_immediate_addressing_mode_exists():
    """
    Objective:
    Move the immediate mode code from CPU.step() to this function.

    Create in addressing_modes.py:
        def immediate(cpu):
            ...

    What it does:
    - Read the next byte from the CPU bus.
    - Move PC to the next position.
    - Return that byte.

    Example:
    A9 42 means LDA #$42.
    The value 0x42 is just after the opcode.
    """
    cpu = make_cpu()

    assert hasattr(addressing_modes, "immediate")
    assert callable(addressing_modes.immediate)
    assert list(inspect.signature(addressing_modes.immediate).parameters) == ["cpu"]
    assert cpu is not None


def test_absolute_addressing_mode_exists():
    """
    Objective:
    Move the absolute mode code from CPU.step() to this function.

    Create in addressing_modes.py:
        def absolute(cpu):
            ...

    What it does:
    - Read the next two bytes from the CPU bus.
    - The first byte is low.
    - The second byte is high.
    - read that address with cpu bus
    - return value inside the address

    Example:
    AD 34 12 means LDA $1234.
    $1234 contains 0x80
    The function must return 0x80.
    """
    cpu = make_cpu()

    assert hasattr(addressing_modes, "absolute")
    assert callable(addressing_modes.absolute)
    assert list(inspect.signature(addressing_modes.absolute).parameters) == ["cpu"]
    assert cpu is not None


"""
At this point, code inside cpu step should have something like:
    ...
    ...
    if opcode == 0xA9: # LDA Inmediate
        self.a = immediate(self)
        self._update_zero_and_negative_flags(self.a)
        return

    elif opcode == 0xAD: # LDA Absolute
        self.a = absolute(self)
        self._update_zero_and_negative_flags(self.a)
        return
    ...
        
"""
