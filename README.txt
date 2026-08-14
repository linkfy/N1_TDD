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
[x] PPU NMI request on VBlank when enabled
[x] CPU stack helpers and shared interrupt flag constants
[x] CPU bus PRG-space write routing through mapper/FakeROM
[x] Mapper000 ignores valid PRG ROM writes for compatibility
[x] CPU-side interrupt_nmi mechanics
[x] Console coordinator consumes PPU NMI request exactly once
[x] Opcode base cycle table metadata
[x] CPU.step returns base instruction cycles
[ ] Console.step advances PPU by CPU cycles * 3

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
Use CPU.step() cycle returns to let Console.step() advance the PPU at the NES
CPU:PPU timing ratio before adding pygame rendering or controller input.

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


Next tutorial step:

Step 268) Console.step advances PPU by CPU cycles * 3
	Files:
		emulator/console.py
		emulator/ppu/ppu.py
		emulator/cpu/cpu.py

	Behavior:
		Console.step() executes one CPU instruction, receives its base CPU cycle count,
		advances the PPU by cpu_cycles * 3, then consumes any PPU NMI request.

	Goal:
		Connect CPU execution time to PPU time progression so frame loops can move
		toward real VBlank/NMI behavior.

	Important:
		Use the existing boundary:
			CPU.step() returns CPU cycles
			PPU.step(cycles) advances PPU time
			Console connects them using 1 CPU cycle = 3 PPU cycles
		Do not add dynamic CPU cycle penalties in this step.
		Do not add rendering, pygame, APU, or controller input in this step.
		Do not add controller input until basic VBlank/NMI progression exists.

After Phase 6:
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
