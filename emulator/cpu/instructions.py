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

def tax(cpu: CPU):
    cpu.x = cpu.a
    cpu._update_zero_and_negative_flags(cpu.x)
    
def txa(cpu: CPU):
    cpu.a = cpu.x
    cpu._update_zero_and_negative_flags(cpu.a)

def tay(cpu: CPU):
    cpu.y = cpu.a
    cpu._update_zero_and_negative_flags(cpu.y)

def tya(cpu: CPU):
    cpu.a = cpu.y
    cpu._update_zero_and_negative_flags(cpu.a)

def adc(cpu: CPU, value: int):
    # Get actual carry status
    carry = int(cpu.flags.get_carry_flag())
    
    a = cpu.a
    result = a + value + carry
    result_8 = result & 0xFF

    # Update flags
    cpu.flags.set_carry_flag(result > 0xFF)
    cpu.flags.set_zero_flag(result_8 == 0)
    cpu.flags.set_negative_flag((result_8 & 0b1000_0000) != 0)

    # https://www.nesdev.org/wiki/Instruction_reference#ADC -> overflow formula
    overflow = ((result_8 ^ a) & (result_8 ^ value)) & 0b1000_0000 # 0b1000_0000 = 0x80
    cpu.flags.set_overflow_flag(overflow != 0)
    
    # Set new A value
    cpu.a = result_8


def sbc(cpu: CPU, value: int):
    
    # Get actual carry status
    carry = int(cpu.flags.get_carry_flag())
    
    a = cpu.a
    # ~value -> inverted should be limited to 8 bits
    # Be careful to not use directly ~value in python, ~0x01 == -2, and we expect 0xFE
    # We can use (~value) & 0xFF | Also we can use: value ^ 0xFF
    value_inverted = (~value) & 0xFF
    result = a + value_inverted + carry
    result_8 = result & 0xFF

    # Update flags
    # Result will never be negative if we use value_inverted, 
    # so is better to test (result > 0xFF) instead of ~(result < 0x00)
    cpu.flags.set_carry_flag(result > 0xFF)
    cpu.flags.set_zero_flag(result_8 == 0)
    cpu.flags.set_negative_flag((result_8 & 0b1000_0000) != 0)

    # https://www.nesdev.org/wiki/Instruction_reference#SBC -> overflow formula
    overflow = ((result_8 ^ a) & (result_8 ^ value_inverted)) & 0b1000_0000 # 0b1000_0000 = 0x80
    cpu.flags.set_overflow_flag(overflow != 0)
    
    # Set new A value
    cpu.a = result_8

def inc(cpu: CPU, address: int):
    value = cpu.bus.read(address)
    result = value + 1
    result_8 = result & 0xFF

    # Set flags
    cpu.flags.set_negative_flag((result_8 & 0b1000_0000) != 0)
    cpu.flags.set_zero_flag(result_8 == 0)

    # Set value on address
    cpu.bus.write(address, result_8)


def dec(cpu: CPU, address: int):
    value = cpu.bus.read(address)
    result = value - 1
    result_8 = result & 0xFF

    # Set flags
    cpu.flags.set_negative_flag((result_8 & 0b1000_0000) != 0)
    cpu.flags.set_zero_flag(result_8 == 0)

    # Set value on address
    cpu.bus.write(address, result_8)



