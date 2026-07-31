from typing import Optional
from dataclasses import dataclass, field
from emulator.memory.vram import VRAM
from emulator.cartridge.mapper_interface import MapperInterface

PPU_ADDRESS_MASK = 0x3FFF # Highest vram address

CHR_START = 0x0000
CHR_END = 0x1FFF

@dataclass
class PpuBus():
    """Routes PPU address-space reads/write"""
    vram: VRAM = field(default_factory=VRAM)
    mapper: Optional[MapperInterface] = None
    
    def read(self, addr: int) -> int:
        addr = addr & PPU_ADDRESS_MASK
        
        if CHR_START <= addr <= CHR_END:
            if self.mapper is not None:
                return self.mapper.read_chr(addr)
            else:
                return self.vram.read(addr)

        return self.vram.read(addr)
    
    def write(self, addr: int, value: int) -> None:
        addr = addr & PPU_ADDRESS_MASK

        if CHR_START <= addr <= CHR_END:
            if self.mapper is not None:
                # Future implementation self.mapper.write_chr()
                raise ValueError("CHR writes are not supported yet")

            self.vram.write(addr, value)
            return
        self.vram.write(addr, value)
        
