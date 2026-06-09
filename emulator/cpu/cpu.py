from dataclasses import dataclass

from emulator.bus.cpu_bus import CpuBus

@dataclass
class CPU:
    bus: CpuBus
    
    # Initial Registers with default value
    a: int = 0
    x: int = 0
    y: int = 0
    pc: int = 0xFFFC
    s: int = 0xFD # -3
    p: int = 0

    # Get one byte from bus and increment pc
    def fetch_byte(self) -> int:
        value = self.bus.read(self.pc)
        self.pc += 1
        return value

    def fetch_word(self) -> int:
        low = self.fetch_byte()
        high = self.fetch_byte()

        return low | (high << 8)
