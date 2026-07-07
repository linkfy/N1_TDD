from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from emulator.cpu.cpu import CPU
# ------------------------------------

from emulator.cpu.instructions import lda
from emulator.cpu.addressing_modes import (
    immediate,
    zero_page,
    zero_page_x,
    absolute,
    absolute_x,
    absolute_y,
    indirect_x,
    indirect_y,
)
# Opcode Handlers include: decoding/addressing details
# They are not the same as instructions

def lda_immediate(cpu: CPU):
    lda(cpu, immediate(cpu))

def lda_zero_page(cpu: CPU):
    addr = zero_page(cpu)
    value = cpu.bus.read(addr)
    lda(cpu, value)

def lda_absolute(cpu: CPU):
    addr = absolute(cpu)
    value = cpu.bus.read(addr)
    lda(cpu, value)

def lda_absolute_x(cpu: CPU):
    addr = absolute_x(cpu)
    value = cpu.bus.read(addr)
    lda(cpu, value)

def lda_absolute_y(cpu: CPU):
    addr = absolute_y(cpu)
    value = cpu.bus.read(addr)
    lda(cpu, value)

def lda_zero_page_x(cpu: CPU):
    addr = zero_page_x(cpu)
    value = cpu.bus.read(addr)
    lda(cpu, value)

def lda_indirect_x(cpu: CPU):
    addr = indirect_x(cpu)
    value = cpu.bus.read(addr)
    lda(cpu, value)

def lda_indirect_y(cpu: CPU):
    addr = indirect_y(cpu)
    value = cpu.bus.read(addr)
    lda(cpu, value)

OPCODE_TABLE = {
    0xA9: lda_immediate,
    0xA5: lda_zero_page,
    0xB5: lda_zero_page_x,
    0xAD: lda_absolute,
    0xBD: lda_absolute_x,
    0xB9: lda_absolute_y,
    0xA1: lda_indirect_x,
    0xB1: lda_indirect_y,
}
