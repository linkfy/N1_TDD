from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from emulator.cpu.cpu import CPU
# --------------

from dataclasses import dataclass

CARRY_FLAG = 1 << 0
ZERO_FLAG = 1 << 1
OVERFLOW_FLAG = 1 << 6
NEGATIVE_FLAG = 1 << 7

@dataclass
class FlagsHandler:
    cpu: CPU

    def _set_zero_flag(self, enabled: bool):
        if enabled:
            self.cpu.p |= ZERO_FLAG 
        else:
            self.cpu.p &= ~ZERO_FLAG

    def _set_negative_flag(self, enabled: bool):
        if enabled:
            self.cpu.p |= NEGATIVE_FLAG
        else:
            self.cpu.p &= ~NEGATIVE_FLAG

    def _set_overflow_flag(self, enabled: bool):
        if enabled:
            self.cpu.p |= OVERFLOW_FLAG
        else:
            self.cpu.p &= ~OVERFLOW_FLAG

    def _set_carry_flag(self, enabled: bool):
        if enabled:
            self.cpu.p |= CARRY_FLAG
        else:
            self.cpu.p &= ~CARRY_FLAG

    def _get_zero_flag(self) -> bool:
        return bool(self.cpu.p & ZERO_FLAG)

    def _get_negative_flag(self) -> bool:
        return bool(self.cpu.p & NEGATIVE_FLAG)

    def _get_overflow_flag(self) -> bool:
        return bool(self.cpu.p & OVERFLOW_FLAG)

    def _get_carry_flag(self) -> bool:
        return bool(self.cpu.p & CARRY_FLAG)
