from dataclasses import dataclass, field
from emulator.bus.ppu_bus import PpuBus

VBLANK_STARTED =                1 << 7
SPRITE_ZERO_HIT =               1 << 6
SPRITE_OVERFLOW =               1 << 5

## PPUCTRL Bits
CTRL_BASE_NAMETABLE_MASK = 0b0000_0011
CTRL_VRAM_INCREMENT_BY_32 =     1 << 2
CTRL_SPRITE_PATTERN_TABLE =     1 << 3
CTRL_BACKGROUND_PATTERN_TABLE = 1 << 4
CTRL_SPRITE_SIZE_8X16 =         1 << 5
CTRL_MASTER_SLAVE_SELECT =      1 << 6
CTRL_NMI_ENABLE =               1 << 7

## PPUMASK bits
MASK_GRAYSCALE =                1 << 0
MASK_SHOW_BACKGROUND_LEFT_8 =   1 << 1
MASK_SHOW_SPRITES_LEFT_8 =      1 << 2
MASK_SHOW_BACKGROUND =          1 << 3
MASK_SHOW_SPRITES =             1 << 4
MASK_EMPHASIZE_RED =            1 << 5
MASK_EMPHASIZE_GREEN =          1 << 6
MASK_EMPHASIZE_BLUE =           1 << 7

PALETTE_START_ADDR =            0x3F00
PALETTE_END_ADDR =              0x3FFF

## PPU Timing
PPU_CYCLES_PER_SCANLINE = 341
PPU_SCANLINES_PER_FRAME = 262

## VBLANK
PPU_VBLANK_START_SCANLINE = 241
PPU_PRE_RENDER_SCANLINE = 261

# OAM_SIZE: 64 Sprites x 4 bytes
OAM_SIZE = 256

SpriteZeroHitPosition = tuple[int, int]

@dataclass
class PPU:
    ctrl: int = 0       # Bits VPHB SINN (Write)
    mask: int = 0       # Bits BGRs bMmG (Write)
    status: int = 0     # Bits VSO- ---- (Read)
    oam_addr: int = 0   # Bits AAAA AAAA (Write)
    oam_data: int = 0   # Preserved for test compatibility, now: oam
    scroll: int = 0     # Bits XXXX XXXX YYYY YYYY (2 Writes)
    addr: int = 0       # Preserved for test compatibility, now: vram_addr
    data: int = 0       # Preserved for test compatibility, now: ppu_bus.read/write to vram and ppu_data_buffer

    vram_addr: int = 0 # Bits AAAA AAAA AAAA AAAA (2 Writes) Known as "v" internal register
    temp_vram_addr: int = 0 # Known as "t" internal register
    fine_x: int = 0 # Known as "x" internal register
    second_write_toggle: bool = False # Known as "w" internal register

    ppu_bus: PpuBus = field(default_factory=PpuBus)
    oam: bytearray = field(default_factory=lambda: bytearray(OAM_SIZE))
    ppu_data_buffer: int = 0 # Internal PPUDATA read buffer

    cycle: int = 0
    scanline: int = 0
    frame: int = 0
    nmi_requested: bool = False
    sprite_zero_hit_position: SpriteZeroHitPosition | None = None

    def set_sprite_zero_hit_position(self, position: SpriteZeroHitPosition | None) -> None:
        self.sprite_zero_hit_position = position
    
    def step(self, cycles: int = 1) -> None:
        """
        When cycle reaches 341, scanline +=1, cycle = 0
        When scanline reaches 262, scanline = 0, frame += 1
        https://www.nesdev.org/wiki/PPU_rendering#Line-by-line_timing
        """
        for _ in range(cycles):
            self.cycle += 1

            # Set sprite_zero_hit status when PPU timing reaches sprite_zero_hit_position
            if self.sprite_zero_hit_position is not None:
                hit_x, hit_y = self.sprite_zero_hit_position
                # When screen x = 0 -> PPU cycle = 1
                if self.scanline == hit_y and self.cycle == hit_x + 1: # Mapping is self.cycle = x + 1
                    self.status |= SPRITE_ZERO_HIT
                    self.sprite_zero_hit_position = None

            if self.cycle >= PPU_CYCLES_PER_SCANLINE:
                self.cycle = 0
                self.scanline += 1

                if self.scanline >= PPU_SCANLINES_PER_FRAME:
                    self.scanline = 0
                    self.frame += 1

                # VBLANK START -> set VBlank on scanline 241
                if self.scanline == PPU_VBLANK_START_SCANLINE:
                    self.status |= VBLANK_STARTED

                    if self.ctrl & CTRL_NMI_ENABLE:
                        self.nmi_requested = True

                # Pre-render clear -> Unset VBlank on scanline 261
                if self.scanline == PPU_PRE_RENDER_SCANLINE:
                    self.status &= ~VBLANK_STARTED
                    # Clear Sprite 0 HIT for the next frame
                    self.status &= ~SPRITE_ZERO_HIT

        
    def write_register(self, addr: int, value: int) -> None:
        value = value & 0xFF
        match addr:
            case 0x2000: # PPUCTRL Write
                self.ctrl = value
            case 0x2001: # PPUMASK Write
                self.mask = value
            case 0x2003: # OAM ADDR Write
                self.oam_addr = value
            case 0x2004: # OAM DATA Write
                # Keep for old compatibility:
                self.oam_data = value
                # Assign value
                self.oam[self.oam_addr] = value
                self.oam_addr = (self.oam_addr + 1) & 0xFF

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
                # Keep for old compatibility test
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
                self.oam_data = self.oam[self.oam_addr]
                # Preserved for old compatibility
                return self.oam_data
            case 0x2007: # PPU DATA read
                # Palette data is returned immediately
                if PALETTE_START_ADDR <= self.vram_addr <= PALETTE_END_ADDR:
                    value = self.ppu_bus.read(self.vram_addr)
                    # Read buffer is discarded and read from mirror nametable: vram_addr - 0x1000: Example: 0x3F00 -> 0x2F00
                    self.ppu_data_buffer = self.ppu_bus.read(self.vram_addr - 0x1000)
                else:
                    value = self.ppu_data_buffer
                    self.ppu_data_buffer = self.ppu_bus.read(self.vram_addr)
                increment = 32 if self.ctrl & CTRL_VRAM_INCREMENT_BY_32 else 1
                self.vram_addr =  (self.vram_addr + increment) & 0x3FFF # 0x3FFF keeps vram_addr in VRAM SIZE range
                # Preserved self.data for old test compatibility
                self.data = value
                return self.data
            case _:
                raise ValueError(f"Unsupported PPU register read: {addr:04X}")

