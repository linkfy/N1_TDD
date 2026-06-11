from dataclasses import dataclass, field
from typing import Optional

from emulator.memory.memory_device import MemoryDevice
from emulator.memory.ram import RAM

@dataclass
class CpuBus(): 
    program_rom: Optional[MemoryDevice] = None
    ram: RAM = field(default_factory=RAM)

    def read(self, addr: int) -> int:
        """Read from CPU Bus"""
        #Internal RAM
        if 0x0 <= addr <= 0x1FFF:
            return self.ram.read(addr & 0x07FF)
        if 0x8000 <= addr <= 0xFFFF:
            if self.program_rom is None: # Ensure rom exists (connected)
                raise ValueError("No program ROM attached")
            return self.program_rom.read(addr - 0x8000)

        raise ValueError(f"Unsupported CPU bus read: {addr:04X}")

   
    def write(self, addr: int, value: int) -> None:
        """ Write to CPU Bus"""
        # Value should be 8 bits
    
        #Internal RAM
        if 0x0 <= addr <= 0x1FFF:
            self.ram.write(addr & 0x07FF, value) 
            return

        raise ValueError(f"Unsupported CPU bus write: {addr:04X}")

