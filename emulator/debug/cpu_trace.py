from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from emulator.cpu.cpu import CPU

# ----------------------------------


def format_cpu_trace(cpu: CPU):
    opcode = cpu.bus.read(cpu.pc)
    return f"{cpu.pc:04X} {opcode:02X} A:{cpu.a:02X} X:{cpu.x:02X} Y:{cpu.y:02X} P:{cpu.p:02X} S:{cpu.s:02X}"

