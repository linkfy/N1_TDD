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
[x] Controller state object for A/B/Select/Start/Up/Down/Left/Right
[x] Controller captures button state and exposes serial read behavior
[x] CpuBus routes $4016 writes to controller strobe
[x] CpuBus routes $4016 reads to controller serial data
[x] Controller strobe behavior captures button state
[x] Controller reads shift one button bit at a time
[x] VALIDATION: CPU program can read controller bits from $4016

Phase 10)
Manual main.py execution path:
[x] main.py loads a local .nes path, calls CPU.reset(), and steps frames
[x] main.py displays background framebuffer with pygame
[x] Connect pygame keyboard input to controller state after pure controller protocol is tested
[x] main.py reports useful frame/opcode/bus errors without requiring a debugger

Phase 11 / Chapter 09)
Sprite rendering:
[x] Define OAM sprite entry constants and SpriteEntry dataclass
[x] Decode one OAM sprite entry
[x] Define sprite attribute constants and SpriteAttributes dataclass
[x] Decode sprite attributes: palette ID, priority, horizontal flip, vertical flip
[x] Build sprite palettes from PPU palette RAM $3F10-$3F1F
[x] Render one 8x8 sprite into framebuffer data
[x] Render all 64 OAM sprites without sprite 0 hit/overflow
[x] Composite background and sprites into one framebuffer
[x] Add Console full-frame/background+sprites framebuffer helper
[x] main.py uses Console.render_framebuffer() for background+sprites display
[x] Add background opacity mask for sprite/background priority
[x] Thread background opacity mask through sprite rendering pipeline
[x] Use sprite priority bit 5 with background opacity mask in pure sprite renderer
[x] Add PPU-level background opacity mask extraction helper
[x] Wire Console.render_framebuffer() to pass the background opacity mask

Phase 12 / Chapter 10)
Performance and manual runtime:
[x] Add periodic FPS counter to main.py
[x] Improve pygame framebuffer drawing/upload path
[x] Add explicit PyPy launchers for manual execution
[ ] Add expected-speed control so manual emulation does not run faster than NES speed
[ ] Optional later: evaluate Numba or other acceleration only if simpler optimizations are not enough

--
Next Steps:

Goal:
Prioritize a working main.py/manual execution path for Mapper000/NROM ROMs while
preserving the linear pytest tutorial flow and avoiding later refactors.

Immediate direction:
	Manual ROM execution now reaches visible background output, sprite rendering,
	keyboard input, and sprite/background priority behavior.

	The next focus is manual runtime performance and observability. The manual runner
	now prints FPS, pygame drawing uses a faster upload/blit path, and explicit PyPy
	launchers exist for manual runs. Next, cap execution to NES speed when the emulator
	becomes fast enough.

	Do not prioritize opcode diagnostics or broad CPU rewrites right now. Performance
	work should be incremental and evidence-driven from the manual FPS signal.

Working main.py means:
	- a developer can provide a local .nes file path manually
	- the emulator boots from the ROM reset vector
	- Console can step frame-by-frame
	- the visual runner displays background + sprites with priority behavior
	- the terminal reports enough FPS information to judge performance changes
	- unsupported I/O does not crash when the missing system is intentionally out of scope
	- tests remain synthetic and do not require commercial ROM files

Manual core validator command:
	uv run python core_validator.py

Expected behavior:
	core_validator.py is a long-running manual ROM execution tool. It will keep
	stepping frames and will not exit by itself. Press Ctrl+C to stop it. This is
	expected and should not be treated as a hang if frame/debug output keeps moving.

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
	- Reference local MarioBros.nes MD5 used during tutorial development:
		5d7bcc400a2fb5fa27346da345d3bb62  MarioBros.nes
	  This is only a reference for manual experiments. Users must provide their own
	  legal copy, and hashes may differ between dumps/revisions.

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

Sprite policy:
	Start with data decoding before drawing.
	OAMDMA remains CPU-bus behavior; sprite rendering reads PPU.oam.
	Do not implement sprite 0 hit or sprite overflow yet.
	Do not make pygame part of sprite rendering. Sprite rendering should produce pure
	Framebuffer data, and main.py should only display that data.

Performance policy:
	Start with a simple manual signal before deep profiling: print FPS from main.py
	every few seconds.

	PyPy is a supported manual runtime target through explicit launcher files. Do not
	change the project's default Python interpreter yet; keep PyPy opt-in for manual
	runs.

	Pygame performance work belongs in manual/frontend helpers such as tools/ and
	main.py. It must not introduce pygame into emulator core modules.

	Expected-speed control belongs in main.py/manual runtime code. The emulator core
	should remain deterministic stepping/rendering logic and should not sleep.

	Potential future acceleration such as Numba should be considered only after:
		1. PyPy manual execution is available,
		2. FPS is visible,
		3. pygame drawing has been improved,
		4. remaining bottlenecks are understood.


Next tutorial step:

Step 318) Add expected-speed control so manual emulation does not run faster than NES speed
	Files:
		main.py
		tests/chapter_10_performance/test_318_main_frame_pacing.py

	Behavior:
		main.py should cap the manual frontend loop to approximately NES NTSC speed when
		the emulator is able to run faster than real time.

		Target:
			NES_NTSC_FPS = 60.0988
			TARGET_FRAME_SECONDS = 1.0 / NES_NTSC_FPS

		Important: frame pacing only sleeps when the completed frame was faster than the
		target. It does not make slow emulation faster.

	Goal:
		prevent manual execution from running faster than real NES speed after renderer
		or runtime improvements.

	Existing reset-vector evidence:
		CPU.reset() already exists in emulator/cpu/cpu.py.
		Reset vector behavior is covered by:
			tests/chapter_01_cpu/test_008_cpu_reset_vector.py
		Cartridge/Mapper000 reset-vector boot is already validated by:
			tests/chapter_02_rom_loading/test_223_VALIDATION_cpu_executes_tiny_ines_rom.py

	Important:
		Do not commit MarioBros.nes or any commercial ROM fixture.
		Automated tests must not call main() or open a pygame window.
		Expected-speed control belongs in the manual frontend path, not emulator core.
		The emulator core should not call time.sleep().

	After this:
		Step 319) Optional later: evaluate Numba or other acceleration if needed.
		Step 320) Optional later: add more detailed profiling if FPS is still too low.

After Phase 6:
	- Phase 7: pure rendering pipeline plus manual pygame smoke runner
	- Phase 8 / Chapter 06: ROM startup preparation
	- Phase 9 / Chapter 07: controller $4016 behavior
	- Phase 10: manual main.py execution path
	- Phase 11 / Chapter 09: sprite rendering

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
