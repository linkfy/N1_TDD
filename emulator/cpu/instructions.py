from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from emulator.cpu.cpu import CPU

# ----------------------------------

def lda(cpu: CPU, value):
    cpu.a = value
    cpu._update_zero_and_negative_flags(cpu.a)


