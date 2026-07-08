from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from emulator.cpu.cpu import CPU

# ----------------------------------

def lda(cpu: CPU, value):
    cpu.a = value
    cpu._update_zero_and_negative_flags(cpu.a)

def sta(cpu: CPU, address: int):
    value = cpu.a
    cpu.bus.write(address, value)

def ldx(cpu: CPU, value):
    cpu.x = value
    cpu._update_zero_and_negative_flags(cpu.x)

def stx(cpu: CPU, address: int):
    value = cpu.x
    cpu.bus.write(address, value)

def ldy(cpu: CPU, value):
    cpu.y = value
    cpu._update_zero_and_negative_flags(cpu.y)

def sty(cpu: CPU, address: int):
    value = cpu.y
    cpu.bus.write(address, value)
