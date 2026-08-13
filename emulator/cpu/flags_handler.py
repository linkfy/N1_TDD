from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from emulator.cpu.cpu import CPU
# --------------

from dataclasses import dataclass

CARRY_FLAG =        1 << 0
ZERO_FLAG =         1 << 1
INTERRUPT_FLAG =    1 << 2
DECIMAL_FLAG =      1 << 3
B_FLAG =            1 << 4
ONE_FLAG =          1 << 5
OVERFLOW_FLAG =     1 << 6
NEGATIVE_FLAG =     1 << 7

@dataclass
class FlagsHandler:
    cpu: CPU

    def set_zero_flag(self, enabled: bool):
        if enabled:
            self.cpu.p |= ZERO_FLAG 
        else:
            self.cpu.p &= ~ZERO_FLAG

    def set_negative_flag(self, enabled: bool):
        if enabled:
            self.cpu.p |= NEGATIVE_FLAG
        else:
            self.cpu.p &= ~NEGATIVE_FLAG

    def set_overflow_flag(self, enabled: bool):
        if enabled:
            self.cpu.p |= OVERFLOW_FLAG
        else:
            self.cpu.p &= ~OVERFLOW_FLAG

    def set_carry_flag(self, enabled: bool):
        if enabled:
            self.cpu.p |= CARRY_FLAG
        else:
            self.cpu.p &= ~CARRY_FLAG

    def set_interrupt_disable_flag(self, enabled: bool):
        if enabled:
            self.cpu.p |= INTERRUPT_FLAG
        else:
            self.cpu.p &= ~INTERRUPT_FLAG

    def set_break_flag(self, enabled: bool):
        if enabled:
            self.cpu.p |= B_FLAG
        else:
            self.cpu.p &= ~B_FLAG
    
    def set_one_flag(self, enabled: bool):
        if enabled:
            self.cpu.p |= ONE_FLAG
        else:
            self.cpu.p &= ~ONE_FLAG
    
    def set_decimal_flag(self, enabled: bool):
        if enabled:
            self.cpu.p |= DECIMAL_FLAG
        else:
            self.cpu.p &= ~DECIMAL_FLAG

    def get_zero_flag(self) -> bool:
        return bool(self.cpu.p & ZERO_FLAG)

    def get_negative_flag(self) -> bool:
        return bool(self.cpu.p & NEGATIVE_FLAG)

    def get_overflow_flag(self) -> bool:
        return bool(self.cpu.p & OVERFLOW_FLAG)

    def get_carry_flag(self) -> bool:
        return bool(self.cpu.p & CARRY_FLAG)

    def get_interrupt_disable_flag(self) -> bool:
        return bool(self.cpu.p & INTERRUPT_FLAG)

    def get_break_flag(self) -> bool:
        return bool(self.cpu.p & B_FLAG)
    
    def get_one_flag(self) -> bool:
        return bool(self.cpu.p & ONE_FLAG)

    def get_decimal_flag(self) -> bool:
        return bool(self.cpu.p & DECIMAL_FLAG)


