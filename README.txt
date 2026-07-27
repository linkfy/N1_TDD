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
PPUADDR / PPUDATA write path:

Goal:
Allow CPU writes to PPU memory through PPU registers.

Important registers:
$2006 PPUADDR
	- first write sets high byte of internal PPU address
	- second write sets low byte of internal PPU address

$2007 PPUDATA
	- writes value to current PPU memory address
	- then increments internal PPU address

Required new PPU state:
	vram_addr
	addr_latch
	ppu_memory / vram placeholder

Basic behavior:
	write_register($2006, high)
	write_register($2006, low)
	write_register($2007, value)

Example:
	write $20 to $2006
	write $00 to $2006
	write $AA to $2007

Result:
	PPU memory[$2000] == $AA

Important:
	Keep this simple first.
	Do not implement full nametable mirroring, palette mirroring, rendering,
	or PPUDATA read buffering yet.

After that:
	- PPU memory map
	- Decode one CHR tile
	- Render one pattern table as debug image
---------------------------------------------
Future Notes:
	- Implement PPUSTATUS:
		- Sprote 0 Hit flag behavior:
				- Required:
					background rendering
					sprite rendering
					pixel overlap detection
					PPU timing
		- Sprite Overflow flag behavior:
				- Required:
					OAM memory
					sprite evaluation per scanline
					more than 8 sprites on a scanline
					quirky NES behavior (buggy real hardware behavior)

