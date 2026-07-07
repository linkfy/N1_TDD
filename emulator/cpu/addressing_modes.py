from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from emulator.cpu.cpu import CPU

# -----------------------------------

def immediate(cpu: CPU) -> int:
    return cpu.fetch_byte()

def absolute(cpu: CPU) -> int:
    addr = cpu.fetch_word()
    return addr  

def absolute_x(cpu: CPU) -> int:
    base = cpu.fetch_word()
    addr = base + cpu.x
    return addr

def absolute_y(cpu: CPU) -> int:
    base = cpu.fetch_word()
    addr = base + cpu.y
    return addr

def zero_page(cpu: CPU) -> int:
    addr = cpu.fetch_byte()
    return addr

def zero_page_x(cpu: CPU) -> int:
    base = cpu.fetch_byte()
    addr = (base + cpu.x) & 0xFF
    # Alternative:
    # addr = (base + cpu.x) % 256 
    return addr





