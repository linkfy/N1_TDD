from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from emulator.cpu.cpu import CPU

# -----------------------------------

def immediate(cpu: CPU) -> int:
    return cpu.fetch_byte()

def absolute(cpu: CPU) -> int:
    addr = cpu.fetch_word()
    return cpu.bus.read(addr)




