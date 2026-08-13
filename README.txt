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

Phase 6)
PPU timing, VBlank, and NMI readiness:
[x] PPU timing counters: cycle, scanline, frame
[x] PPU VBlank generation from timing
[x] PPU pre-render VBlank clear from timing
[ ] PPU NMI request on VBlank when enabled
[ ] CPU/system integration consumes PPU NMI request

Phase 7)
Rendering pipeline and pygame frontend:
[ ] Define pure framebuffer data shape
[ ] Convert color-index grids to RGB/framebuffer data without pygame
[ ] Render pattern table/debug graphics into framebuffer data
[ ] Render nametable background into framebuffer data
[ ] Add palette color lookup
[ ] Add basic frame loop using PPU timing/VBlank
[ ] Add thin pygame frontend that displays framebuffer data
[ ] Add manual pygame smoke runner
[ ] Add sprites/OAMDMA later

Phase 8)
Controller input:
[ ] Controller state object for A/B/Select/Start/Up/Down/Left/Right
[ ] CpuBus routes $4016 writes to controller strobe
[ ] CpuBus routes $4016 reads to controller serial data
[ ] Controller strobe behavior latches button state
[ ] Controller reads shift one button bit at a time
[ ] Validate CPU program can read controller bits from $4016
[ ] Connect pygame keyboard input to controller state

--
Next Steps:

Goal:
Add enough PPU time progression for future ROMs to run frame loops before adding
pygame rendering or controller input.

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

Rendering policy:
	Do not add image-output/debug-image generation now.
	Do not add pygame yet.
	Pygame rendering can be introduced later when the emulator has enough timing
	and frame-loop behavior to make visual output useful.

Pygame/testing policy for Phase 7:
	Keep pygame outside the emulator core.
	The emulator core should produce pure framebuffer data.
	Pygame should be a thin frontend that displays that framebuffer.

	Tests should focus on pure data transformations, for example:
		color-index grid -> RGB/framebuffer data
		pattern table grid -> framebuffer data
		nametable data -> framebuffer data

	Avoid tests that depend on a real pygame window.
	Manual pygame smoke runners are acceptable for visual confirmation.

	Preferred boundary:
		emulator/ppu or emulator/rendering:
			pure rendering/framebuffer functions

		emulator/frontend or tools:
			pygame window, event loop, keyboard, display upload

	The emulator core should still be importable/testable without pygame.

Controller policy:
	Do not add controller input before basic VBlank/NMI progression exists.
	Controller $4016 behavior becomes useful after games can run frame loops and
	there is a rendering path where input effects can be observed.


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
	- Phase 6: PPU timing, VBlank, and NMI readiness
	- Phase 7: pure rendering pipeline plus thin pygame frontend
	- Phase 8: controller $4016 behavior

Controller phase outline:
	Controller state stores 8 buttons in NES read order:
		A, B, Select, Start, Up, Down, Left, Right

	CPU write $4016 controls strobe/latch behavior.
	CPU read $4016 returns one button bit at a time.
	Pygame keyboard input should only be connected after the pure controller
	protocol is tested.
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
