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
[ ] Audit old PpuBus tests to avoid direct internal vram assumptions
[ ] Palette RAM mapping refinement
[ ] Nametable VRAM mapping refinement
[ ] CHR ROM/RAM mapper refinement
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

Goal:
Complete safe PPU memory-map refinement and then decode CHR graphics data.

Important rule:
Do not implement sprite 0 hit or sprite overflow yet. Those require rendering,
sprite evaluation, OAM timing, and pixel overlap behavior.

Stubbing policy:
Avoid broad fake stubs for systems that are part of the tutorial path.
PPU behavior should be implemented intentionally, not faked.
Audio/APU can be stubbed later because audio is out of tutorial scope.

Compatibility rule:
Before changing PpuBus internals, make sure old tests assert public behavior via:
	ppu_bus.read(addr)
	ppu_bus.write(addr, value)

Avoid old tests depending on:
	ppu_bus.vram.read(addr)
	ppu_bus.vram.write(addr, value)

except in the VRAM-specific test.

Step 252) Audit old PpuBus-facing tests for public API usage
	Files to inspect:
		tests/chapter_03_ppu_registers/test_235_ppu_bus_vram_read_write.py
		tests/chapter_03_ppu_registers/test_242_ppudata_writes_through_ppu_bus.py
		tests/chapter_03_ppu_registers/test_249_ppudata_read_buffer.py
		tests/chapter_03_ppu_registers/test_250_ppudata_palette_read_exception.py

	Goal:
		Old tests should verify bus behavior, not internal storage layout.

	Allowed:
		assert ppu_bus.read(addr) == value

	Avoid:
		assert ppu_bus.vram.read(addr) == value

Step 253) Palette RAM mapping refinement
	File:
		emulator/bus/ppu_bus.py

	Goal:
		Make $3F00-$3FFF route to palette RAM instead of big VRAM.

	Behavior:
		palette RAM has 32 bytes
		$3F20-$3FFF mirrors $3F00-$3F1F
		special mirrors:
			$3F10 -> $3F00
			$3F14 -> $3F04
			$3F18 -> $3F08
			$3F1C -> $3F0C

Step 254) Nametable VRAM mapping refinement
	File:
		emulator/bus/ppu_bus.py

	Goal:
		Move $2000-$3EFF from big VRAM behavior toward nametable behavior.

	Initial behavior:
		2KB nametable VRAM
		$2000-$2FFF maps into that VRAM
		$3000-$3EFF mirrors $2000-$2EFF

	Later refinement:
		cartridge mirroring modes: horizontal, vertical, four-screen, etc.

Step 255) CHR ROM/RAM mapper refinement
	Files:
		emulator/cartridge/mapper_interface.py
		emulator/cartridge/mapper000.py
		emulator/bus/ppu_bus.py

	Goal:
		Keep $0000-$1FFF routed through mapper.
		Add CHR RAM write behavior only when mapper.write_chr is introduced.

	Important:
		Do not make CHR ROM writable.
		CHR RAM support should be explicit.

Step 256) Decode one CHR tile
	File:
		emulator/ppu/chr_decoder.py or similar

	Behavior:
		decode 16 CHR bytes into an 8x8 grid of color indices 0-3

After Phase 5:
	- Render one pattern table as debug image
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
