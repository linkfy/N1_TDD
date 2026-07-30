from dataclasses import dataclass, field

from emulator.bus.ppu_bus import PpuBus

VBLANK_STARTED = 1 << 7
SPRITE_ZERO_HIT = 1 << 6
SPRITE_OVERFLOW = 1 << 5

## PPUCTRL Bits
CTRL_VRAM_INCREMENT_BY_32 = 1 << 2


@dataclass
class PPU:
    ctrl: int = 0       # Bits VPHB SINN (Write)
    mask: int = 0       # Bits BGRs bMmG (Write)
    status: int = 0     # Bits VSO- ---- (Read)
    oam_addr: int = 0   # Bits AAAA AAAA (Write)
    oam_data: int = 0   # Bits DDDD DDDD (Read/Write)
    scroll: int = 0     # Bits XXXX XXXX YYYY YYYY (2 Writes)
    addr: int = 0       # Preserved for test compatibility, now: vram_addr
    data: int = 0       # Bits DDDD DDDD (Read/Write)

    vram_addr: int = 0 # Bits AAAA AAAA AAAA AAAA (2 Writes) Known as "v" internal register
    temp_vram_addr: int = 0 # Known as "t" internal register
    fine_x: int = 0 # Known as "x" internal register
    second_write_toggle: bool = False # Known as "w" internal register

    ppu_bus: PpuBus = field(default_factory=PpuBus)

    
    def write_register(self, addr: int, value: int) -> None:
        value = value & 0xFF
        match addr:
            case 0x2000: # PPUCTRL Write
                self.ctrl = value
            case 0x2001: # PPUSTATUS Write
                self.mask = value
            case 0x2003: # OAM ADDR Write
                self.oam_addr = value
            case 0x2004: # OAM DATA Write
                self.oam_data = value
            case 0x2005: # PPU SCROLL Write
                # Keep for old compatibility
                self.scroll = value
                # https://www.nesdev.org/wiki/PPU_scrolling#$2005_(PPUSCROLL)_first_write_(w_is_0)
                if not self.second_write_toggle:
                    # PPU Scroll first write:
                    # x register: save last 3 bits  | x:              FGH <- d: .....FGH
                    self.fine_x = value & 0b000_0111
                    # t register: save 5 first bits | t: ....... ...ABCDE <- d: ABCDE...
                    self.temp_vram_addr = (self.temp_vram_addr & 0b1111_1111_1110_0000) | (value >> 3)
                    # w:                  <- 1
                    self.second_write_toggle = True
                # https://www.nesdev.org/wiki/PPU_scrolling#$2005_(PPUSCROLL)_second_write_(w_is_1)
                else:
                    # t register: | t: FGH..AB CDE..... <- d: ABCDEFGH
                    self.temp_vram_addr = self.temp_vram_addr & 0b1000_1100_0001_1111 # KEEP ONLY UNTOUCHED BITS
                    # Put last 3 bits 0b0000_0111 -> 0b0111_0000_0000_0000 (Move 12 times)
                    self.temp_vram_addr = self.temp_vram_addr | ((value & 0b0000_0111) << 12)
                    # Put first 5 bits 0b1111_1000 -> 0b0000_0011_1110_0000 (Move 2 times)
                    self.temp_vram_addr = self.temp_vram_addr | ((value & 0b1111_1000) << 2)
                    self.second_write_toggle = False
            case 0x2006: # PPU ADDR Write
                # Old behavior (now a placeholder for test compatibility | Not needed):
                self.addr = value
                # New Behavior:
                if not self.second_write_toggle:
                    self.temp_vram_addr = (
                        (self.temp_vram_addr & 0x00FF) | ((value & 0x3F) << 8)
                    )
                    self.second_write_toggle = True
                else:
                    self.temp_vram_addr = (
                        (self.temp_vram_addr & 0x3F00) | value
                    )
                    self.vram_addr = self.temp_vram_addr
                    self.second_write_toggle = False
            case 0x2007: # PPU DATA Write
                self.data = value
                # Write data to Vram addr
                self.ppu_bus.write(self.vram_addr, value)
                # Accessing this register increments vram address
                increment = 32 if self.ctrl & CTRL_VRAM_INCREMENT_BY_32 else 1
                self.vram_addr = (self.vram_addr + increment) & 0x3FFF

            case _:
                raise ValueError(f"Unsupported PPU register write: {addr:04X}")

    def read_register(self, addr: int) -> int:
        match addr:
            case 0x2002: # PPU_STATUS Read
                value = self.status
                # Clear VBLANK before returning old status
                self.status &= ~VBLANK_STARTED            
                self.second_write_toggle = False
                return value
            case 0x2004: # OAM DATA Read
                return self.oam_data
            case 0x2007: # PPU DATA read
                return self.data
            case _:
                raise ValueError(f"Unsupported PPU register read: {addr:04X}")


