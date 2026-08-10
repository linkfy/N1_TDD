from typing import Optional
from dataclasses import dataclass, field
from emulator.memory.vram import VRAM
from emulator.cartridge.mapper_interface import MapperInterface

PPU_ADDRESS_MASK = 0x3FFF # Highest vram address

CHR_START = 0x0000
CHR_END = 0x1FFF

PALETTE_START = 0x3F00
PALETTE_END = 0x3FFF
PALETTE_SIZE = 0x20

NAMETABLE_START = 0x2000
NAMETABLE_END = 0x3EFF 
NAMETABLE_SIZE = 0x800

@dataclass
class PpuBus():
    """Routes PPU address-space reads/write"""
    vram: VRAM = field(default_factory=VRAM)
    mapper: Optional[MapperInterface] = None

    def normalize_palette_addr(self, addr: int) -> int:
        """
        This function ensures that accessing addresses from palette
        ensure mirroring for shared indexes.

        In real hardware PALETTE RAM is another component, 
        we treat it as a part of big VRAM for simplicity,
        """
        index = (addr - PALETTE_START) % PALETTE_SIZE
        # Palette indexes 0x10, 0x14, 0x18, and 0x1C mirror
        # 0x00, 0x04, 0x08, and 0x0C. 
        if index in (0x10, 0x14, 0x18, 0x1C):
            index -= 0x10
        return PALETTE_START + index

    def normalize_nametable_addr(self, addr: int) -> int:
        """
        Nametable: 0x400 Areas of memory with a total of 4 nametables 
        - [0x2000 - 0x23FF], [0x2400 - 0x27FF]
        - [0x2800 - 0x2BFF], [0x2C00 - 0x2FFF]
        - [0x3000...0x3EFF] = Mirrors (Yes, It is not completed to 0x3FFF)
        $3000-$3EFF mirrors $2000-$2EFF and is rarely used directly.
        """

        if 0x3000 <= addr <= 0x3EFF:
            addr -= 0x1000
        index = (addr - 0x2000) % NAMETABLE_SIZE
        return 0x2000 + index
    
    def read(self, addr: int) -> int:
        addr = addr & PPU_ADDRESS_MASK
        
        if CHR_START <= addr <= CHR_END:
            if self.mapper is not None:
                return self.mapper.read_chr(addr)
            else:
                return self.vram.read(addr)

        if NAMETABLE_START <= addr <= NAMETABLE_END:
            return self.vram.read(self.normalize_nametable_addr(addr))


        if PALETTE_START <= addr <= PALETTE_END:
            return self.vram.read(self.normalize_palette_addr(addr))

        return self.vram.read(addr)
    
    def write(self, addr: int, value: int) -> None:
        addr = addr & PPU_ADDRESS_MASK

        if CHR_START <= addr <= CHR_END:
            if self.mapper is not None:
                self.mapper.write_chr(addr, value)
                return
            self.vram.write(addr, value)
            return

        if NAMETABLE_START <= addr <= NAMETABLE_END:
            self.vram.write(self.normalize_nametable_addr(addr), value)
            return

        if PALETTE_START <= addr <= PALETTE_END:
            self.vram.write(self.normalize_palette_addr(addr), value)
            return

        self.vram.write(addr, value)
        
