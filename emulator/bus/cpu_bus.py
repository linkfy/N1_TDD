from dataclasses import dataclass, field
from typing import Optional

from emulator.cartridge.cartridge import Cartridge
from emulator.cartridge.mapper_factory import create_mapper
from emulator.memory.memory_device import MemoryDevice
from emulator.memory.ram import RAM

@dataclass
class CpuBus(): 
    program_rom: Optional[MemoryDevice] = None
    cartridge: Optional[Cartridge] = None
    ram: RAM = field(default_factory=RAM)

    def __post_init__(self):
        # Allow only program_rom(for testing) or cartridge
        if self.program_rom is not None and self.cartridge is not None:
            raise ValueError("Cannot attach both program_rom and cartridge")
        # Define a new mapper
        self.mapper = None
        # Set the right mapper using a factory, 
        # example -> if cartridge.mapper = 0 it uses Mapper000
        if self.cartridge is not None:
            self.mapper = create_mapper(self.cartridge)

    def read(self, addr: int) -> int:
        """Read from CPU Bus"""
        #Internal RAM
        if 0x0 <= addr <= 0x1FFF:
            return self.ram.read(addr & 0x07FF)
        # Program ROM
        if 0x8000 <= addr <= 0xFFFF:
            # Cartridges uses a mapper:
            if self.mapper is not None:
                return self.mapper.read_prg(addr)
            # Fake ROMS uses raw read:
            if self.program_rom is not None: 
                return self.program_rom.read(addr - 0x8000)
            # If not mapper or not program_rom, it fails
            raise ValueError("No program ROM or cartridge attached")
            

        raise ValueError(f"Unsupported CPU bus read: {addr:04X}")

   
    def write(self, addr: int, value: int) -> None:
        """ Write to CPU Bus"""
        # Value should be 8 bits
    
        #Internal RAM
        if 0x0 <= addr <= 0x1FFF:
            self.ram.write(addr & 0x07FF, value) 
            return

        raise ValueError(f"Unsupported CPU bus write: {addr:04X}")

