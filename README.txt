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
[x] Decode one full pattern table
[x] Build pattern table debug grid
[ ] PPU timing counters: cycle, scanline, frame
[ ] PPU VBlank generation from timing
[ ] PPU pre-render VBlank clear from timing
[ ] PPU NMI request on VBlank when enabled
[ ] CPU/system integration consumes PPU NMI request

Phase 6)
Rendering:
Render with pygame later
Render nametable background
Add palette colors
Add frame timing/VBlank/NMI
Add sprites/OAMDMA

--
Next Steps:

Goal:
Add enough PPU time progression for future ROMs to run frame loops before adding
controllers or pygame rendering.

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

Completed CHR graphics data path for this phase:
	decode one 16-byte CHR tile into an 8x8 grid of color indexes 0-3
	validate CHR decode through tiny iNES ROM -> mapper -> PpuBus
	decode one 4096-byte pattern table into 256 decoded tiles
	arrange 256 decoded tiles into a 128x128 pattern table debug grid

Rendering policy:
	Do not add image-output/debug-image generation now.
	Do not add pygame yet.
	Pygame rendering can be introduced later when the emulator has enough timing
	and frame-loop behavior to make visual output useful.

Step 259) PPU timing counters
	File:
		emulator/ppu/ppu.py

	Behavior:
		add explicit PPU time state:
			cycle
			scanline
			frame

		add a small step/tick method that advances PPU time.

	Goal:
		Create the mechanism needed for VBlank and future rendering timing.

	Initial timing model:
		341 PPU cycles per scanline
		262 scanlines per frame

	Important:
		Do not implement rendering, sprite 0 hit, sprite overflow, or odd-frame
		cycle skip in this step.

Step 260) VBlank generation from PPU timing
	File:
		emulator/ppu/ppu.py

	Behavior:
		set VBLANK_STARTED when timing reaches the VBlank start point
		clear VBLANK_STARTED on the pre-render scanline

	Goal:
		Allow ROMs that poll PPUSTATUS $2002 for VBlank to eventually progress.

	Important:
		PPUSTATUS reads should still return the old status and clear VBlank,
		as already implemented.

Step 261) PPU NMI request on VBlank
	Files:
		emulator/ppu/ppu.py
		emulator/cpu/cpu.py or system integration later

	Behavior:
		when VBlank starts and PPUCTRL bit 7 is set, raise an explicit NMI request
		flag such as:
			ppu.nmi_requested = True

	Goal:
		Prepare for games that depend on NMI instead of polling PPUSTATUS.

	Important:
		The PPU can expose the request first.
		Full CPU interrupt consumption can be a separate step.

Step 262) CPU/system integration consumes PPU NMI request
	Files:
		emulator/cpu/cpu.py
		emulator/bus/cpu_bus.py or a future system/console coordinator

	Behavior:
		connect PPU NMI request to CPU NMI handling in a controlled place

	Goal:
		Make frame-based game loops possible before adding controllers.

	Important:
		Do not add controller input until basic VBlank/NMI progression exists.

After Phase 5:
	- Implement controller $4016 behavior
	- Add pygame rendering path
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
