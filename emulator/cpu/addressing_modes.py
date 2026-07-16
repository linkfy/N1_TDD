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

def zero_page_y(cpu: CPU) -> int:
    base = cpu.fetch_byte()
    addr = (base + cpu.y) & 0xFF
    # Alternative:
    # addr = (base + cpu.y) % 256 
    return addr

def indirect(cpu: CPU) -> int:
    ptr = cpu.fetch_word()
    low = cpu.bus.read(ptr)
    # Real hardware bug: If pointer address ends in FF then cpu fails to cross page:
    high_addr = (ptr & 0xFF00) | ((ptr + 1) & 0x00FF)
    # Normal case:  ptr = 0x0200 -> high_addr = 0x0201 
    # Bug case:     ptr = 0x02FF -> high_addr = 0x0200 (Instead of 0x0300)
    high = cpu.bus.read(high_addr)

    return low | (high << 8)

def indirect_x(cpu: CPU) -> int:
    base = cpu.fetch_byte()
    ptr = (base + cpu.x) & 0xFF
    low = cpu.bus.read(ptr)
    high = cpu.bus.read((ptr + 1) & 0xFF)

    return low | (high << 8)

def indirect_y(cpu: CPU) -> int:
    ptr = cpu.fetch_byte()
    low = cpu.bus.read(ptr)
    high = cpu.bus.read((ptr + 1) & 0xFF)
    # Reads the pointer first, then adds Y
    return (low | (high << 8)) + cpu.y

    
def relative(cpu: CPU) -> int:
    offset = cpu.fetch_byte()
    # Transform to signed integer
    # 0x7F -> +127
    # 0x80 -> -128
    # 0xFF -> -1
    if offset & 0x80: # offset has bit 7 active, is negative
        offset -= 0x100
    return offset

