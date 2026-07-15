from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from emulator.cpu.cpu import CPU
# ------------------------------------

from emulator.cpu.instructions import (lda, sta, ldx, stx, ldy, sty, 
                                       tax, txa, tay, tya, 
                                       adc, sbc, inc, dec, inx, dex, iny, dey, 
                                       asl, asl_a, lsr, lsr_a, rol, rol_a, ror, ror_a)
from emulator.cpu.addressing_modes import (
    immediate,
    zero_page,
    zero_page_x,
    zero_page_y,
    absolute,
    absolute_x,
    absolute_y,
    indirect_x,
    indirect_y,
)
# Opcode Handlers include: decoding/addressing details
# They are not the same as instructions

# ------ LDA Opcodes                 
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

# ------ STA Opcodes

def sta_zero_page(cpu: CPU):
    addr = zero_page(cpu) 
    sta(cpu, addr)

def sta_zero_page_x(cpu: CPU):
    addr = zero_page_x(cpu) 
    sta(cpu, addr)

def sta_absolute(cpu: CPU):
    addr = absolute(cpu) 
    sta(cpu, addr)

def sta_absolute_x(cpu: CPU):
    addr = absolute_x(cpu) 
    sta(cpu, addr)

def sta_absolute_y(cpu: CPU):
    addr = absolute_y(cpu) 
    sta(cpu, addr)

def sta_indirect_x(cpu: CPU):
    addr = indirect_x(cpu) 
    sta(cpu, addr)

def sta_indirect_y(cpu: CPU):
    addr = indirect_y(cpu) 
    sta(cpu, addr)

# ------ LDX Opcodes
                 
def ldx_immediate(cpu: CPU):
    ldx(cpu, immediate(cpu))
                 
def ldx_zero_page(cpu: CPU):
    addr = zero_page(cpu)
    value = cpu.bus.read(addr)
    ldx(cpu, value)

def ldx_zero_page_y(cpu: CPU):
    addr = zero_page_y(cpu)
    value = cpu.bus.read(addr)
    ldx(cpu, value)
                 
def ldx_absolute(cpu: CPU):
    addr = absolute(cpu)
    value = cpu.bus.read(addr)
    ldx(cpu, value)
                 
def ldx_absolute_y(cpu: CPU):
    addr = absolute_y(cpu)
    value = cpu.bus.read(addr)
    ldx(cpu, value)

# ------ STX Opcodes

def stx_zero_page(cpu: CPU):
    addr = zero_page(cpu) 
    stx(cpu, addr)


def stx_zero_page_y(cpu: CPU):
    addr = zero_page_y(cpu) 
    stx(cpu, addr)


def stx_absolute(cpu: CPU):
    addr = absolute(cpu) 
    stx(cpu, addr)

# ------ LDY Opcodes
                 
def ldy_immediate(cpu: CPU):
    ldy(cpu, immediate(cpu))
                 
def ldy_zero_page(cpu: CPU):
    addr = zero_page(cpu)
    value = cpu.bus.read(addr)
    ldy(cpu, value)

def ldy_zero_page_x(cpu: CPU):
    addr = zero_page_x(cpu)
    value = cpu.bus.read(addr)
    ldy(cpu, value)
                 
def ldy_absolute(cpu: CPU):
    addr = absolute(cpu)
    value = cpu.bus.read(addr)
    ldy(cpu, value)
                 
def ldy_absolute_x(cpu: CPU):
    addr = absolute_x(cpu)
    value = cpu.bus.read(addr)
    ldy(cpu, value)

# ------ STY Opcodes

def sty_zero_page(cpu: CPU):
    addr = zero_page(cpu) 
    sty(cpu, addr)


def sty_zero_page_x(cpu: CPU):
    addr = zero_page_x(cpu) 
    sty(cpu, addr)


def sty_absolute(cpu: CPU):
    addr = absolute(cpu) 
    sty(cpu, addr)


# ------ ADC Opcodes

def adc_immediate(cpu: CPU):
    value = immediate(cpu)
    adc(cpu, value)

def adc_zero_page(cpu: CPU):
    addr = zero_page(cpu)
    value = cpu.bus.read(addr)
    adc(cpu, value)

def adc_zero_page_x(cpu: CPU):
    addr = zero_page_x(cpu)
    value = cpu.bus.read(addr)
    adc(cpu, value)

def adc_absolute(cpu: CPU):
    addr = absolute(cpu)
    value = cpu.bus.read(addr)
    adc(cpu, value)

def adc_absolute_x(cpu: CPU):
    addr = absolute_x(cpu)
    value = cpu.bus.read(addr)
    adc(cpu, value)

def adc_absolute_y(cpu: CPU):
    addr = absolute_y(cpu)
    value = cpu.bus.read(addr)
    adc(cpu, value)

def adc_indirect_x(cpu: CPU):
    addr = indirect_x(cpu)
    value = cpu.bus.read(addr)
    adc(cpu, value)

def adc_indirect_y(cpu: CPU):
    addr = indirect_y(cpu)
    value = cpu.bus.read(addr)
    adc(cpu, value)


# ------ SBC Opcodes

def sbc_immediate(cpu: CPU):
    value = immediate(cpu)
    sbc(cpu, value)

def sbc_zero_page(cpu: CPU):
    addr = zero_page(cpu)
    value = cpu.bus.read(addr)
    sbc(cpu, value)

def sbc_zero_page_x(cpu: CPU):
    addr = zero_page_x(cpu)
    value = cpu.bus.read(addr)
    sbc(cpu, value)

def sbc_absolute(cpu: CPU):
    addr = absolute(cpu)
    value = cpu.bus.read(addr)
    sbc(cpu, value)

def sbc_absolute_x(cpu: CPU):
    addr = absolute_x(cpu)
    value = cpu.bus.read(addr)
    sbc(cpu, value)

def sbc_absolute_y(cpu: CPU):
    addr = absolute_y(cpu)
    value = cpu.bus.read(addr)
    sbc(cpu, value)

def sbc_indirect_x(cpu: CPU):
    addr = indirect_x(cpu)
    value = cpu.bus.read(addr)
    sbc(cpu, value)

def sbc_indirect_y(cpu: CPU):
    addr = indirect_y(cpu)
    value = cpu.bus.read(addr)
    sbc(cpu, value)

# ------ INC Opcodes

def inc_zero_page(cpu: CPU):
    addr = zero_page(cpu)
    inc(cpu, addr)

def inc_zero_page_x(cpu: CPU):
    addr = zero_page_x(cpu)
    inc(cpu, addr)

def inc_absolute(cpu: CPU):
    addr = absolute(cpu)
    inc(cpu, addr)

def inc_absolute_x(cpu: CPU):
    addr = absolute_x(cpu)
    inc(cpu, addr)


# ------ DEC Opcodes

def dec_zero_page(cpu: CPU):
    addr = zero_page(cpu)
    dec(cpu, addr)

def dec_zero_page_x(cpu: CPU):
    addr = zero_page_x(cpu)
    dec(cpu, addr)

def dec_absolute(cpu: CPU):
    addr = absolute(cpu)
    dec(cpu, addr)

def dec_absolute_x(cpu: CPU):
    addr = absolute_x(cpu)
    dec(cpu, addr)

# ------ ASL Opcodes
# asl_a -> directly mapped on OPCODE_TABLE

def asl_zero_page(cpu: CPU):
    addr = zero_page(cpu)
    asl(cpu, addr)

def asl_zero_page_x(cpu: CPU):
    addr = zero_page_x(cpu)
    asl(cpu, addr)

def asl_absolute(cpu: CPU):
    addr = absolute(cpu)
    asl(cpu, addr)

def asl_absolute_x(cpu: CPU):
    addr = absolute_x(cpu)
    asl(cpu, addr)


# ------ LSR Opcodes
# lsr_a -> directly mapped on OPCODE_TABLE

def lsr_zero_page(cpu: CPU):
    addr = zero_page(cpu)
    lsr(cpu, addr)

def lsr_zero_page_x(cpu: CPU):
    addr = zero_page_x(cpu)
    lsr(cpu, addr)

def lsr_absolute(cpu: CPU):
    addr = absolute(cpu)
    lsr(cpu, addr)

def lsr_absolute_x(cpu: CPU):
    addr = absolute_x(cpu)
    lsr(cpu, addr)

# ------ ROL Opcodes
# rol_a -> directly mapped on OPCODE_TABLE

def rol_zero_page(cpu: CPU):
    addr = zero_page(cpu)
    rol(cpu, addr)

def rol_zero_page_x(cpu: CPU):
    addr = zero_page_x(cpu)
    rol(cpu, addr)

def rol_absolute(cpu: CPU):
    addr = absolute(cpu)
    rol(cpu, addr)

def rol_absolute_x(cpu: CPU):
    addr = absolute_x(cpu)
    rol(cpu, addr)

# ------ ROR Opcodes
# ror_a -> directly mapped on OPCODE_TABLE

def ror_zero_page(cpu: CPU):
    addr = zero_page(cpu)
    ror(cpu, addr)

def ror_zero_page_x(cpu: CPU):
    addr = zero_page_x(cpu)
    ror(cpu, addr)

def ror_absolute(cpu: CPU):
    addr = absolute(cpu)
    ror(cpu, addr)

def ror_absolute_x(cpu: CPU):
    addr = absolute_x(cpu)
    ror(cpu, addr)







OPCODE_TABLE = {
    0xA9: lda_immediate,
    0xA5: lda_zero_page,
    0xB5: lda_zero_page_x,
    0xAD: lda_absolute,
    0xBD: lda_absolute_x,
    0xB9: lda_absolute_y,
    0xA1: lda_indirect_x,
    0xB1: lda_indirect_y,

    0x85: sta_zero_page,
    0x95: sta_zero_page_x,
    0x8D: sta_absolute,
    0x9D: sta_absolute_x,
    0x99: sta_absolute_y,
    0x81: sta_indirect_x,
    0x91: sta_indirect_y,

    0xA2: ldx_immediate,
    0xA6: ldx_zero_page,
    0xB6: ldx_zero_page_y,
    0xAE: ldx_absolute,
    0xBE: ldx_absolute_y,
    
    0x86: stx_zero_page,
    0x96: stx_zero_page_y,
    0x8E: stx_absolute,

    0xA0: ldy_immediate,
    0xA4: ldy_zero_page,
    0xB4: ldy_zero_page_x,
    0xAC: ldy_absolute,
    0xBC: ldy_absolute_x,

    0x84: sty_zero_page,
    0x94: sty_zero_page_x,
    0x8C: sty_absolute,
    
    0xAA: tax,
    0x8A: txa,
    0xA8: tay,
    0x98: tya,

    0x69: adc_immediate,
    0x65: adc_zero_page,
    0x75: adc_zero_page_x,
    0x6D: adc_absolute,
    0x7D: adc_absolute_x,
    0x79: adc_absolute_y,
    0x61: adc_indirect_x,
    0x71: adc_indirect_y,

    0xE9: sbc_immediate,
    0xE5: sbc_zero_page,
    0xF5: sbc_zero_page_x,
    0xED: sbc_absolute,
    0xFD: sbc_absolute_x,
    0xF9: sbc_absolute_y,
    0xE1: sbc_indirect_x,
    0xF1: sbc_indirect_y,

    0xE6: inc_zero_page,
    0xF6: inc_zero_page_x,
    0xEE: inc_absolute,
    0xFE: inc_absolute_x,
    
    0xC6: dec_zero_page,
    0xD6: dec_zero_page_x,
    0xCE: dec_absolute,
    0xDE: dec_absolute_x,

    0xE8: inx,
    0xCA: dex,
    0xC8: iny,
    0x88: dey,

    0x0A: asl_a,
    0x06: asl_zero_page,
    0x16: asl_zero_page_x,
    0x0E: asl_absolute,
    0x1E: asl_absolute_x,

    0x4A: lsr_a,
    0x46: lsr_zero_page,
    0x56: lsr_zero_page_x,
    0x4E: lsr_absolute,
    0x5E: lsr_absolute_x,

    0x2A: rol_a,
    0x26: rol_zero_page,
    0x36: rol_zero_page_x,
    0x2E: rol_absolute,
    0x3E: rol_absolute_x,

    0x6A: ror_a,
    0x66: ror_zero_page,
    0x76: ror_zero_page_x,
    0x6E: ror_absolute,
    0x7E: ror_absolute_x,


}
