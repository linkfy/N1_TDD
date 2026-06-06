from dataclasses import dataclass, field
from emulator.memory.ram import RAM

@dataclass
class CpuBus():
    ...
    ram: RAM = field(default_factory=RAM)

    def read(self, addr: int) -> int:
        """Read from CPU Bus"""
        #Internal RAM
        if 0x0 <= addr <= 0x1FFF:
            return self.ram.read(addr & 0x07FF)

        raise ValueError(f"Unsupported CPU bus read: {addr:04X}")

   
    def write(self, addr: int, value: int) -> None:
        """ Write to CPU Bus"""
        # Value should be 8 bits
    
        #Internal RAM
        if 0x0 <= addr <= 0x1FFF:
            self.ram.write(addr & 0x07FF, value) 
            return

        raise ValueError(f"Unsupported CPU bus write: {addr:04X}")

