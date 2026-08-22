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
[x] Console.step advances PPU by CPU cycles * 3
[x] VALIDATION: tiny CPU program reaches VBlank NMI through Console.step

Phase 7)
Rendering pipeline and pygame frontend:
[x] Define pure framebuffer data shape
[x] Framebuffer get_pixel/set_pixel helpers
[x] Convert color-index grids to RGB/framebuffer data without pygame
[x] Render pattern table/debug graphics into framebuffer data
[x] Define minimal NES RGB palette approximation
[x] Render pattern table/debug graphics using default NES palette
[x] Render nametable background into framebuffer data
[x] Render nametable background using default NES palette
[x] Decode attribute table palette selection for tile coordinates
[x] Render nametable background using attribute-selected palettes
[x] Build background palettes from PPU palette RAM bytes
[x] Render nametable background using palette RAM bytes
[x] Extract current PPU background memory into framebuffer data
[x] Console exposes current background framebuffer data
[x] VALIDATION: CPU writes PPU memory then Console renders framebuffer
[x] Add basic frame loop helper using PPU frame counter
[x] Add manual pygame framebuffer display helpers
[x] Add manual pygame smoke runner main loop
[x] Add sprites later [Nothing to do]

Phase 8 / Chapter 06)
ROM startup preparation:
[x] Add explicit APU/audio no-op register behavior for out-of-scope audio addresses
[x] Implement OAMDMA $4014 copy into PPU OAM without sprite rendering yet

Phase 9 / Chapter 07)
Controller input:
[ ] Controller state object for A/B/Select/Start/Up/Down/Left/Right
[ ] Controller captures button state and exposes serial read behavior
[ ] CpuBus routes $4016 writes to controller strobe
[ ] CpuBus routes $4016 reads to controller serial data
[ ] Controller strobe behavior latches button state
[ ] Controller reads shift one button bit at a time
[ ] Validate CPU program can read controller bits from $4016

Phase 10)
Manual main.py execution path:
[ ] main.py loads a local .nes path, calls CPU.reset(), and steps frames
[ ] main.py reports useful frame/opcode/bus errors without requiring a debugger
[ ] Connect pygame keyboard input to controller state after pure controller protocol is tested

--
Next Steps:

Goal:
Prioritize a working main.py/manual execution path for Mapper000/NROM ROMs while
preserving the linear pytest tutorial flow and avoiding later refactors.

Immediate direction:
	Chapter 06 now owns ROM startup preparation: explicit APU/audio no-op behavior
	and OAMDMA $4014. These are completed because they let real NROM startup code
	continue through common bus accesses without pretending audio or sprites are
	fully implemented.

	Do not prioritize opcode diagnostics right now. Keep that as a future debugging
	improvement after the bus-visible startup behavior is less crash-prone.

Working main.py means:
	- a developer can provide a local .nes file path manually
	- the emulator boots from the ROM reset vector
	- Console can step frame-by-frame
	- unsupported I/O does not crash when the missing system is intentionally out of scope
	- tests remain synthetic and do not require commercial ROM files

Local ROM policy for manual main.py runs:
	- The tutorial repository does not include commercial ROM files.
	- If a student/developer wants to manually try Mario Bros., they must provide
	  their own legal copy as:
		MarioBros.nes
	- This file is intentionally ignored by git.
	- Any Mario Bros. `.nes` file that uses Mapper000/NROM should exercise the same
	  mapper path, though exact ROM hashes may differ between dumps/revisions.
	- To record the local file hash, run:
		md5sum MarioBros.nes
	- Local known MarioBros.nes MD5:
		TODO: fill from `md5sum MarioBros.nes` on the developer machine.
	  This assistant session can see the file exists, but cannot execute md5sum with
	  the currently available tools.

Important rule:
Do not implement sprite 0 hit or sprite overflow yet. Those require rendering,
sprite evaluation, OAM timing, and pixel overlap behavior.

Stubbing policy:
Avoid broad fake stubs for systems that are part of the tutorial path.
PPU behavior should be implemented intentionally, not faked.
Audio/APU can be stubbed later because audio is out of tutorial scope.

For main.py survival:
	- APU/audio register writes may become explicit no-ops because audio is out of scope.
	- Controller $4016 should be implemented intentionally, not faked.
	- OAMDMA $4014 should be implemented intentionally, even before sprite rendering.
	- Avoid broad catch-all CpuBus handlers that hide real unsupported addresses.

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
	Pygame is allowed only in manual/frontend entry points such as tools/ or main.py.
	The emulator core continues to produce pure Framebuffer data.

Pygame/testing policy for Phase 7:
	Keep pygame outside the emulator core.
	The emulator core should produce pure framebuffer data.
	Pygame should only appear in manual/frontend entry points such as tools/ or main.py.

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
	Basic VBlank/NMI progression and frame stepping now exist.
	Controller $4016 can be prioritized soon because local ROM experiments already
	reach controller-addressing paths.
	Implement the real strobe/latch/shift behavior rather than fake button reads.
	Controller tests should start in chapter 07 after the chapter 06 ROM startup
	preparation tests.


Next tutorial step:

Step 290) Start controller input with a pure Controller state object
	Files:
		emulator/input/controller.py
		emulator/input/__init__.py
		tests/chapter_07_controller_input/test_290_controller_definition.py

	Behavior:
		Define button state and NES serial-read order without wiring pygame or CpuBus yet.

	Goal:
		keep controller input as a pure, testable mechanism before connecting it to
		CPU address $4016.

	Existing reset-vector evidence:
		CPU.reset() already exists in emulator/cpu/cpu.py.
		Reset vector behavior is covered by:
			tests/chapter_01_cpu/test_008_cpu_reset_vector.py
		Cartridge/Mapper000 reset-vector boot is already validated by:
			tests/chapter_02_rom_loading/test_223_VALIDATION_cpu_executes_tiny_ines_rom.py

	Important:
		Do not commit MarioBros.nes or any commercial ROM fixture.
		Use generated bytes/FakeROM in automated tests.
		Do not connect pygame yet.
		Do not route $4016 through CpuBus yet.
		Do not fake controller reads with a constant 0.
		Pygame may be used later by main.py, but emulator core modules must stay pygame-free.

	After this:
		Step 291) Add controller capture/strobe/serial-read behavior using
		          tests/chapter_07_controller_input/test_291_controller_capture_and_serial_read.py.
		Step 292) Route CpuBus $4016 writes/reads to Controller.
		Step 293) Validate a CPU program can read controller bits from $4016.
		Step 294) Add main.py manual ROM boot loop using CPU.reset() and
		          Console.step_until_next_frame(max_cpu_instructions=...).

After Phase 6:
	- Phase 7: pure rendering pipeline plus manual pygame smoke runner
	- Phase 8 / Chapter 06: ROM startup preparation
	- Phase 9 / Chapter 07: controller $4016 behavior
	- Phase 10: manual main.py execution path

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
