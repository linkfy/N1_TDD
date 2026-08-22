from dataclasses import dataclass, field
from typing import Optional

from emulator.cartridge.cartridge import Cartridge
from emulator.cartridge.mapper_factory import create_mapper
from emulator.memory.memory_device import MemoryDevice
from emulator.memory.ram import RAM
from emulator.ppu.ppu import PPU
from emulator.input.controller import Controller

@dataclass
class CpuBus(): 
    program_rom: Optional[MemoryDevice] = None
    cartridge: Optional[Cartridge] = None
    ram: RAM = field(default_factory=RAM)
    ppu: PPU = field(default_factory=PPU)
    controller_1: Controller = field(default_factory=Controller)

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
            # Connect the mapper also to ppu_bus: bus.mapper <-> bus.ppu.ppu_bus.mapper
            self.ppu.ppu_bus.mapper = self.mapper

    def read(self, addr: int) -> int:
        """Read from CPU Bus"""
        #Internal RAM
        if 0x0 <= addr <= 0x1FFF:
            return self.ram.read(addr & 0x07FF)
        # PPU Registers
        if 0x2000 <= addr <= 0x3FFF:
            unmirrored_addr = 0x2000 + ((addr - 0x2000) % 8)
            return self.ppu.read_register(unmirrored_addr)
       
        #! APU Registers: Out of scope
        if 0x4000 <= addr <= 0x4013:
            return 0
        if addr == 0x4015:
            return 0

        # Controller port 1
        if addr == 0x4016:
            return self.controller_1.read_bit()

        # Controller port 2: Out of scope
        if addr == 0x4017:
            return 0
 

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

        # PPU Registers
        if 0x2000 <= addr <= 0x3FFF:
            unmirrored_addr = 0x2000 + ((addr - 0x2000) % 8)
            self.ppu.write_register(unmirrored_addr, value)
            return
        
        # OAMDMA: copy one CPU page into PPU OAM
        if addr == 0x4014:
            page_start = (value & 0xFF) << 8

            for offset in range(256):
                self.ppu.oam[offset] = self.read(page_start + offset)
            return

        #! APU Registers: Out of scope
        if 0x4000 <= addr <= 0x4013:
            return
        if addr == 0x4015:
            return 

        # Controller port 1
        if addr == 0x4016:
            self.controller_1.write_strobe(value)
            return

        # Controller port 2: Out of scope
        if addr == 0x4017:
            return

        # PROGRAM ROM
        if 0x8000 <= addr <= 0xFFFF:
            if self.mapper is not None:
                self.mapper.write_prg(addr, value)
                return
            # For old program_rom=FakeROM tests 
            if self.program_rom is not None:
                self.program_rom.write(addr - 0x8000, value)
                return

        raise ValueError(f"Unsupported CPU bus write: {addr:04X}")

