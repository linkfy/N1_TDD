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
PPU registers, PPU bus, and first graphics data path:
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
[x] PPU internal registers: vram_addr, temp_vram_addr, fine_x, second_write_toggle
[x] PPUADDR two-write behavior using temp_vram_addr
[x] PPUSTATUS read resets second_write_toggle
[x] PPUDATA write path through PpuBus
[x] PPUCTRL bit 2 controls PPUDATA increment by 1 or 32
[x] Tiny validation ROM writes PPU memory through PPUADDR/PPUDATA
[x] PPUSCROLL two-write behavior using temp_vram_addr/fine_x
[x] PPUCTRL remaining bit constants
[x] PPUMASK bit constants
[x] OAM memory and OAMADDR/OAMDATA behavior
[x] PPUDATA read behavior and read buffer
[x] Palette read exception for PPUDATA
[x] Connect cartridge mapper to PPU bus
[x] Palette RAM mapping using big VRAM backing
[x] Nametable VRAM mapping using big VRAM backing
[x] CHR write routing through mapper.write_chr
[x] Decode one CHR tile
[x] Validate CHR tile decode from tiny iNES ROM through mapper/PpuBus
[ ] Decode one full pattern table
[ ] Build pattern table debug grid

Phase 6)
Rendering:
Render one pattern table as debug image
Render nametable background
Add palette colors
Add frame timing/VBlank/NMI
Add sprites/OAMDMA

--
Next Steps:

Goal:
Move from decoding one CHR tile to decoding a full pattern table, then build a
debug grid that can become the first visual output.

Important rule:
Do not implement sprite 0 hit or sprite overflow yet. Those require rendering,
sprite evaluation, OAM timing, and pixel overlap behavior.

Stubbing policy:
Avoid broad fake stubs for systems that are part of the tutorial path.
PPU behavior should be implemented intentionally, not faked.
Audio/APU can be stubbed later because audio is out of tutorial scope.

Compatibility rule:
Old tutorial steps may document the implementation shape they introduced.
For example, the original PpuBus VRAM test may mention direct vram access because
that step teaches the first simple backing store.

From the current PPU memory-map refinement onward, new tests should prefer public
PpuBus behavior via:
	ppu_bus.read(addr)
	ppu_bus.write(addr, value)

Avoid new tests depending on:
	ppu_bus.vram.read(addr)
	ppu_bus.vram.write(addr, value)

unless the test is intentionally about the low-level VRAM memory device or an old
historical teaching step.

Storage policy for this phase:
Keep using the existing large VRAM backing object for PpuBus storage.
Do not move palette RAM or nametable RAM into separate storage classes yet.

Completed PPU memory-map behavior for this phase:
	$0000-$1FFF routes CHR reads/writes through mapper when mapper exists
	$3F10 should behave like $3F00
	$3F20 should behave like $3F00
	$3000 should behave like $2000

The physical Python storage may still be the large VRAM array.

Step 257A) Decode one full pattern table
	File:
		emulator/ppu/chr_decoder.py or similar

	Behavior:
		decode 4096 CHR bytes into 256 decoded 8x8 tiles

	Goal:
		A pattern table is 256 tiles.
		Each tile is 16 bytes.
		4096 bytes / 16 bytes = 256 tiles.

		This is still not rendering a screen or image file.
		It only proves we can decode all tiles from one pattern table.

	Suggested shape:
		decode_pattern_table(pattern_table_bytes: bytes) -> list[list[list[int]]]

	Important:
		CHR ROM remains read-only for official Mapper000/NROM in this tutorial.
		CHR RAM and unlicensed/homebrew Mapper000 variants are out of scope for now.

Step 257B) Build pattern table debug grid
	File:
		emulator/ppu/chr_decoder.py or emulator/ppu/pattern_table.py

	Behavior:
		arrange 256 decoded tiles into a 128x128 grid of color indexes 0-3

	Goal:
		A pattern table debug view is 16 tiles across by 16 tiles down.
		Each tile is 8x8 pixels.
		16 * 8 = 128 pixels wide and high.

		This gives a screen-like data grid before RGB colors, image files,
		windows, nametables, scrolling, or timing.

	Suggested shape:
		build_pattern_table_debug_grid(decoded_tiles) -> list[list[int]]

After Phase 5:
	- Convert pattern table debug grid into an image/debug display
	- Render nametable background
---------------------------------------------
Future Notes:

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
