[x] Phase 1) 
CPU:
- Declare Registers
- Flags
- Address Mode
- Instructions

[x] Phase 2)
Memory Map:
- RAM
- Cartridge dummy 

[x] Phase 3)
Debug trace
iNES parser file parser .nes
	
[x] Phase 4)
NROM mapper (No Bank Switch)

Phase 5)
PPU Registers dummy
PPU (Basic)
PPUSTATUS VBLANK behavior
PPUADDR/PPUDATA write path
PPU memory map
Decode one CHR tile

Phase 6)
Rendering:
Render one pattern table as debug image
Render nametable background
Add palette colors
Add frame timing/VBlank/NMI
Add sprites/OAMDMA

--
Next Steps:
Write PPU Status side effects:
Define 	VBLANK_STARTED
		SPRITE_ZERO_HIT
		SPRITE_OVERFLOW

Clear VBlank on status read
		value = self.status
		self.status &= ~VBLANK_STARTED
		return value

!! PPUSTATUS read return old value, then clears VBLANK



