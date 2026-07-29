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
PPU / PPU bus basics:
[x] PPU register dataclass fields
[x] PPU write_register/read_register basics
[x] CpuBus routes $2000-$3FFF to PPU registers
[x] Tiny validation ROM writes PPUCTRL/PPUMASK
[x] PPUSTATUS flag constants
[x] PPUSTATUS VBLANK behavior on read
[x] VRAM memory device
[x] MapperInterface protocol
[x] PpuBus basic shape, address mask, VRAM backing
[x] PpuBus CHR-area read routing through mapper
[x] PPU owns PpuBus
[ ] PPUADDR internal address latch
[ ] PPUSTATUS read resets address latch
[ ] PPUDATA write path through PpuBus
[ ] PPU memory map refinement
[ ] Decode one CHR tile

Phase 6)
Rendering:
Render one pattern table as debug image
Render nametable background
Add palette colors
Add frame timing/VBlank/NMI
Add sprites/OAMDMA

--
Next Steps:

PPUSCROLL two-write behavior
PPUDATA read behavior
PPUDATA read buffer
palette read exception
PPUCTRL nametable bits interaction with address state
PPUMASK flags/constants
PPUSTATUS sprite bits behavior later
OAMDATA/OAMADDR behavior


After that:
	- PPU memory map
	- Decode one CHR tile
	- Render one pattern table as debug image
---------------------------------------------
Future Notes:

Connect cartridge mapper to PPU bus
Meaning when CpuBus(cartridge=...) creates the mapper, the PPU-side bus should also receive it:
self.mapper = create_mapper(self.cartridge)
self.ppu.ppu_bus.mapper = self.mapper
That will allow:
PPU $0000-$1FFF -> mapper.read_chr(...)
and prepares for CHR tile decoding / first pixels.

	- Implement PPUSTATUS:
		- Sprite 0 Hit flag behavior:
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
