from dataclasses import dataclass, field

from emulator.bus.ppu_bus import PpuBus

VBLANK_STARTED = 1 << 7
SPRITE_ZERO_HIT = 1 << 6
SPRITE_OVERFLOW = 1 << 5

@dataclass
class PPU:
    ctrl: int = 0       # Bits VPHB SINN (Write)
    mask: int = 0       # Bits BGRs bMmG (Write)
    status: int = 0     # Bits VSO- ---- (Read)
    oam_addr: int = 0   # Bits AAAA AAAA (Write)
    oam_data: int = 0   # Bits DDDD DDDD (Read/Write)
    scroll: int = 0     # Bits XXXX XXXX YYYY YYYY (2 Writes)
    addr: int = 0       # Bits AAAA AAAA AAAA AAAA (2 Writes)
    data: int = 0       # Bits DDDD DDDD (Read/Write)

    ppu_bus: PpuBus = field(default_factory=PpuBus)

    
    def write_register(self, addr: int, value: int) -> None:
        value = value & 0xFF
        match addr:
            case 0x2000:
                self.ctrl = value
            case 0x2001:
                self.mask = value
            case 0x2003:
                self.oam_addr = value
            case 0x2004:
                self.oam_data = value
            case 0x2005:
                self.scroll = value
            case 0x2006:
                self.addr = value
            case 0x2007:
                self.data = value
            case _:
                raise ValueError(f"Unsupported PPU register write: {addr:04X}")

    def read_register(self, addr: int) -> int:
        match addr:
            case 0x2002: # PPU_STATUS
                value = self.status
                # Clear VBLANK before returning old status
                self.status &= ~VBLANK_STARTED                
                return value
            case 0x2004:
                return self.oam_data
            case 0x2007:
                return self.data
            case _:
                raise ValueError(f"Unsupported PPU register read: {addr:04X}")


