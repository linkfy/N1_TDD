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

def inx(cpu: CPU):
    result = cpu.x + 1
    result_8 = result & 0xFF

    # Set flags
    cpu.flags.set_negative_flag((result_8 & 0b1000_0000) != 0)
    cpu.flags.set_zero_flag(result_8 == 0)

    cpu.x = result_8

def dex(cpu: CPU):
    result = cpu.x - 1
    result_8 = result & 0xFF

    # Set flags
    cpu.flags.set_negative_flag((result_8 & 0b1000_0000) != 0)
    cpu.flags.set_zero_flag(result_8 == 0)

    cpu.x = result_8


def iny(cpu: CPU):
    result = cpu.y + 1
    result_8 = result & 0xFF

    # Set flags
    cpu.flags.set_negative_flag((result_8 & 0b1000_0000) != 0)
    cpu.flags.set_zero_flag(result_8 == 0)

    cpu.y = result_8

def dey(cpu: CPU):
    result = cpu.y - 1
    result_8 = result & 0xFF

    # Set flags
    cpu.flags.set_negative_flag((result_8 & 0b1000_0000) != 0)
    cpu.flags.set_zero_flag(result_8 == 0)

    cpu.y = result_8

def asl(cpu: CPU, addr: int):
    value = cpu.bus.read(addr)
    result = value << 1
    result_8 = result & 0xFF

    # Set flags
    cpu.flags.set_carry_flag((value & 0b1000_0000) != 0)
    cpu.flags.set_negative_flag((result_8 & 0b1000_0000) != 0)
    cpu.flags.set_zero_flag(result_8 == 0)

    cpu.bus.write(addr, result_8)

def asl_a(cpu: CPU):
    value = cpu.a
    result = value << 1
    result_8 = result & 0xFF

    # Set flags
    cpu.flags.set_carry_flag((value & 0b1000_0000) != 0)
    cpu.flags.set_negative_flag((result_8 & 0b1000_0000) != 0)
    cpu.flags.set_zero_flag(result_8 == 0)

    cpu.a = result_8



def lsr(cpu: CPU, addr: int):
    value = cpu.bus.read(addr)
    result = value >> 1
    result_8 = result & 0xFF

    # Set flags
    cpu.flags.set_carry_flag((value & 0x01) != 0)
    cpu.flags.set_negative_flag(False)
    cpu.flags.set_zero_flag(result_8 == 0)

    cpu.bus.write(addr, result_8)

def lsr_a(cpu: CPU):
    value = cpu.a
    result = value >> 1
    result_8 = result & 0xFF

    # Set flags
    cpu.flags.set_carry_flag((value & 0x01) != 0)
    cpu.flags.set_negative_flag(False)
    cpu.flags.set_zero_flag(result_8 == 0)

    cpu.a = result_8


def rol(cpu: CPU, addr: int):
    value = cpu.bus.read(addr)
    old_carry = int(cpu.flags.get_carry_flag())

    result = (value << 1) | old_carry
    result_8 = result & 0xFF

    # Set flags

    cpu.flags.set_carry_flag((value & 0b1000_0000) != 0)
    cpu.flags.set_zero_flag(result_8 == 0)
    cpu.flags.set_negative_flag((result_8 & 0b1000_0000) != 0)

    cpu.bus.write(addr, result_8)


def rol_a(cpu: CPU):
    value = cpu.a
    old_carry = int(cpu.flags.get_carry_flag())

    result = (value << 1) | old_carry
    result_8 = result & 0xFF

    # Set flags

    cpu.flags.set_carry_flag((value & 0b1000_0000) != 0)
    cpu.flags.set_zero_flag(result_8 == 0)
    cpu.flags.set_negative_flag((result_8 & 0b1000_0000) != 0)

    cpu.a = result_8

def ror(cpu: CPU, addr: int):
    value = cpu.bus.read(addr)
    old_carry = int(cpu.flags.get_carry_flag())

    result = (value >> 1) | (old_carry << 7)
    result_8 = result & 0xFF

    # Set flags

    cpu.flags.set_carry_flag((value & 0x1) != 0)
    cpu.flags.set_zero_flag(result_8 == 0)
    cpu.flags.set_negative_flag((result_8 & 0b1000_0000) != 0)

    cpu.bus.write(addr, result_8)

def ror_a(cpu: CPU):
    value = cpu.a
    old_carry = int(cpu.flags.get_carry_flag())

    result = (value >> 1) | (old_carry << 7)
    result_8 = result & 0xFF

    # Set flags

    cpu.flags.set_carry_flag((value & 0x1) != 0)
    cpu.flags.set_zero_flag(result_8 == 0)
    cpu.flags.set_negative_flag((result_8 & 0b1000_0000) != 0)

    cpu.a = result_8

def and_a(cpu: CPU, value: int):
    result_8 = (cpu.a & value) & 0xFF
    
    # Flags:
    cpu.flags.set_zero_flag(result_8 == 0)
    cpu.flags.set_negative_flag((result_8 & 0b1000_0000) != 0)

    cpu.a = result_8


def or_a(cpu: CPU, value: int):
    result_8 = (cpu.a | value) & 0xFF
    
    # Flags:
    cpu.flags.set_zero_flag(result_8 == 0)
    cpu.flags.set_negative_flag((result_8 & 0b1000_0000) != 0)

    cpu.a = result_8

def or_e(cpu: CPU, value: int):
    result_8 = (cpu.a ^ value) & 0xFF
    
    # Flags:
    cpu.flags.set_zero_flag(result_8 == 0)
    cpu.flags.set_negative_flag((result_8 & 0b1000_0000) != 0)

    cpu.a = result_8


def bit(cpu: CPU, value: int):
    result_8 = (cpu.a & value) & 0xFF
    
    # Flags:
    cpu.flags.set_zero_flag(result_8 == 0)
    cpu.flags.set_negative_flag((value & 0b1000_0000) != 0)
    cpu.flags.set_overflow_flag((value & 0b0100_0000) != 0)

def cmp(cpu: CPU, value: int):
    result_8 = (cpu.a - value) & 0xFF

    # Flags:
    cpu.flags.set_carry_flag(cpu.a >= value)
    cpu.flags.set_zero_flag(cpu.a == value)
    cpu.flags.set_negative_flag((result_8 & 0b1000_0000) !=0)


def cpx(cpu: CPU, value: int):
    result_8 = (cpu.x - value) & 0xFF

    # Flags:
    cpu.flags.set_carry_flag(cpu.x >= value)
    cpu.flags.set_zero_flag(cpu.x == value)
    cpu.flags.set_negative_flag((result_8 & 0b1000_0000) !=0)


def cpy(cpu: CPU, value: int):
    result_8 = (cpu.y - value) & 0xFF

    # Flags:
    cpu.flags.set_carry_flag(cpu.y >= value)
    cpu.flags.set_zero_flag(cpu.y == value)
    cpu.flags.set_negative_flag((result_8 & 0b1000_0000) !=0)

def bcc(cpu: CPU, offset: int):
    if not cpu.flags.get_carry_flag():
        cpu.pc = (cpu.pc + offset) & 0xFFFF

def bcs(cpu: CPU, offset: int):
    if cpu.flags.get_carry_flag():
        cpu.pc = (cpu.pc + offset) & 0xFFFF

def beq(cpu: CPU, offset: int):
    if cpu.flags.get_zero_flag():
        cpu.pc = (cpu.pc + offset) & 0xFFFF

def bne(cpu: CPU, offset: int):
    if not cpu.flags.get_zero_flag():
        cpu.pc = (cpu.pc + offset) & 0xFFFF


def bpl(cpu: CPU, offset: int):
    if not cpu.flags.get_negative_flag():
        cpu.pc = (cpu.pc + offset) & 0xFFFF

def bmi(cpu: CPU, offset: int):
    if cpu.flags.get_negative_flag():
        cpu.pc = (cpu.pc + offset) & 0xFFFF

def bvc(cpu: CPU, offset: int):
    if not cpu.flags.get_overflow_flag():
        cpu.pc = (cpu.pc + offset) & 0xFFFF

def bvs(cpu: CPU, offset: int):
    if cpu.flags.get_overflow_flag():
        cpu.pc = (cpu.pc + offset) & 0xFFFF

def jmp(cpu: CPU, addr: int):
    cpu.pc = addr & 0xFFFF

def jsr(cpu: CPU, addr: int):
    # After fetching opcode + 2-byte operand, PC points to the next instruction.
    # JSR pushes PC-1 because RTS increment the pulled return address to next instruction.
    return_addr = (cpu.pc -1) & 0xFFFF 
    STACK_BASE = 0x0100

    high = (return_addr >> 8) & 0xFF
    low = return_addr & 0xFF

    cpu.bus.write(STACK_BASE | cpu.s, high)
    cpu.s = (cpu.s - 1) & 0xFF

    cpu.bus.write(STACK_BASE | cpu.s, low)
    cpu.s = (cpu.s - 1) & 0xFF
    
    cpu.pc = addr & 0xFFFF

def rts(cpu: CPU):
    STACK_BASE = 0x0100

    cpu.s = (cpu.s + 1) & 0xFF
    low = cpu.bus.read(STACK_BASE | cpu.s)

    cpu.s = (cpu.s + 1) & 0xFF
    high = cpu.bus.read(STACK_BASE | cpu.s)

    addr = (high << 8) | low
    cpu.pc = (addr + 1) & 0xFFFF

def brk(cpu: CPU):
    # Why PC + 1? CPU.step already consumed opcode BRK ($00)
    # So PC points to padding byte after BRK opcode. It can be anything (And ignored)
    # We need to increment PC to the next real instruction, for when we return.
    return_addr = (cpu.pc + 1) & 0xFFFF 
    STACK_BASE = 0x0100

    high = (return_addr >> 8) & 0xFF
    low = return_addr & 0xFF
    # Save return address to stack 
    cpu.bus.write(STACK_BASE | cpu.s, high)
    cpu.s = (cpu.s - 1) & 0xFF

    cpu.bus.write(STACK_BASE | cpu.s, low)
    cpu.s = (cpu.s - 1) & 0xFF

    # Set break flag before saving to stack
    cpu.flags.set_break_flag(True)
    # Save flags to stack
    cpu.bus.write(STACK_BASE | cpu.s, cpu.p)
    cpu.s = (cpu.s - 1) & 0xFF
    # Set interrupt disable flag
    cpu.flags.set_interrupt_disable_flag(True)
    # Clear break flag after saving: B Flag exists only in the flags byte pushed to stack,
    # not as a real state in the CPU
    cpu.flags.set_break_flag(False)

    low = cpu.bus.read(0xFFFE)
    high = cpu.bus.read(0xFFFF)
    cpu.pc = (high << 8) | low

def rti(cpu: CPU):
    STACK_BASE = 0x0100
    
    cpu.s = (cpu.s + 1) & 0xFF
    flags = cpu.bus.read(STACK_BASE | cpu.s)
    #NVxxDIZC bits from stack saved flags
    cpu.p = flags & 0b11001111 
    # Retrieve PC from stack
    cpu.s = (cpu.s + 1) & 0xFF
    low = cpu.bus.read(STACK_BASE | cpu.s)

    cpu.s = (cpu.s + 1) & 0xFF
    high = cpu.bus.read(STACK_BASE | cpu.s)

    cpu.pc = (high << 8) | low


