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
[x] Add expected-speed control so manual emulation does not run faster than NES speed

Phase 13 / Chapter 11)
PPU compatibility / sprite 0 hit:
[x] Clear sprite 0 hit at the simplified pre-render timing boundary
[x] Detect non-transparent sprite 0/background pixel overlap
[x] Let PPU timing set PPUSTATUS sprite 0 hit at a supplied position
[x] Extract sprite 0 overlap position from current PPU state
[x] Console schedules sprite 0 hit before advancing each frame
[x] Manual checkpoint documented for Super Mario Bros. without ROM fixtures

Phase 14 / Chapter 12)
Cartridge nametable mirroring:
[x] Decode horizontal/vertical mirroring from iNES flags 6 bit 0
[x] Preserve mirroring metadata in Cartridge
[x] Preserve mirroring metadata in Mapper000/MapperInterface
[x] Apply horizontal/vertical mirroring in PpuBus nametable normalization
[x] VALIDATION: synthetic nametable reads/writes follow selected mirroring mode

Phase 15 / Chapter 13)
PPU scrolling and background viewport:
[x] Copy PPUCTRL base-nametable bits into temp_vram_addr
[x] Derive coarse/fine background viewport position from PPU scroll state
[ ] Compose a 256x240 framebuffer viewport across two horizontal nametables
[ ] Compose the matching scrolled background opacity mask
[ ] Extract/render adjacent logical nametables from current PPU state
[ ] Integrate the scrolled viewport into Console background/full-frame rendering
[ ] VALIDATION: manually revisit Super Mario Bros. horizontal movement

--
Next Steps:

Goal:
Prioritize a working main.py/manual execution path for Mapper000/NROM ROMs while
preserving the linear pytest tutorial flow and avoiding later refactors.

Immediate direction:
	Manual ROM execution now reaches visible background output, sprite rendering,
	keyboard input, sprite/background priority, paced NES-speed presentation, and
	sprite-0-hit timing behavior.

	The Super Mario Bros. manual checkpoint now progresses beyond the previous
	PPUSTATUS polling stall. The next observed limitation is horizontal background
	scrolling. Cartridge mirroring metadata now reaches PpuBus and horizontal/vertical
	address aliases are tested. The next work is PPU viewport state and rendering.

	Do not prioritize opcode diagnostics or broad CPU rewrites right now. Performance
	work should be incremental and evidence-driven from the manual FPS signal.

Working main.py means:
	- a developer can provide a local .nes file path manually
	- the emulator boots from the ROM reset vector
	- Console can step frame-by-frame
	- the visual runner displays background + sprites with priority behavior
	- sprite 0 hit can unblock games that use PPUSTATUS bit 6 as a timing signal
	- cartridge-backed PpuBus nametable accesses honor horizontal/vertical mirroring
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
	- MarioBros.nes remains the basic manual reference ROM.
	- Super Mario Bros.nes may be used as an additional manual compatibility checkpoint
	  with a user-provided legal copy, especially for sprite 0 hit and future scrolling.
	- No commercial ROM is added to automated tests; all mirroring tests use synthetic
	  headers and PPU memory data.

Important rule:
Sprite 0 hit now has an incremental frame-level implementation. Exact dot-level
accuracy, OAM Y+1, PPUMASK left-edge behavior, x=255 behavior, 8x16 sprites, and
sprite overflow remain separate future accuracy work.

Super Mario Bros. discovery:
	A manual Super Mario Bros. experiment showed the title/menu background and FPS
	continuing, while Mario did not appear, the upper coin/color animation did not
	progress normally, and controls appeared unresponsive.

	Mario Bros. controller input still worked, so the symptom was not treated as proven
	controller failure. At that point the PPU defined SPRITE_ZERO_HIT but never set it.
	Super Mario Bros. uses sprite 0 hit as a timing signal, so the CPU could remain in a
	PPUSTATUS polling loop while emulator frames and FPS continued.

	The implemented path now clears the flag at pre-render, detects overlap from
	explicit opacity data, schedules the position, and lets PPU timing set the status
	bit. No fixed/fake scanline hit was added.

Mirroring discovery:
	Super Mario Bros. can now progress and accept input, but horizontal movement still
	looks incorrect because the background viewport does not scroll yet.

	Before Chapter 12, PpuBus nametable normalization always behaved like vertical
	mirroring:

		$2000 -> A
		$2400 -> B
		$2800 -> A
		$2C00 -> B

	Standard Super Mario Bros. normally declares vertical mirroring, which keeps the
	left/right logical nametables distinct for horizontal scrolling. Chapter 12 now
	decodes, propagates, and applies that cartridge metadata. This fixes memory aliases;
	it does not move the visible viewport.

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
	Sprite 0 hit has a simplified tested timing path. Sprite overflow remains out of
	scope.
	Do not make pygame part of sprite rendering. Sprite rendering should produce pure
	Framebuffer data, and main.py should only display that data.

Mirroring policy:
	Mirroring is cartridge metadata, not a renderer preference. Decode it from the iNES
	header, preserve it through cartridge/mapper ownership, and let PpuBus use it when
	normalizing nametable addresses.

	Bit 0 of iNES flags 6 selects:
		0 -> horizontal mirroring
		1 -> vertical mirroring

	Four-screen mirroring remains out of scope for the first mirroring phase. Do not
	hide the current fixed mapping behind global state or ROM-specific conditions.

Scrolling policy:
	Scrolling is a PPU viewport mechanism, not cartridge mirroring. Keep the phases
	separate even though correct scrolling depends on correct mirrored nametable reads.

	Build scrolling incrementally from the existing PPU t/v/x/w state model:
		1. complete PPUCTRL base-nametable writes into temporary address t
		2. derive coarse/fine viewport coordinates as pure data
		3. render across adjacent logical nametables
		4. integrate the viewport without putting pygame in emulator core

	Do not jump directly to a ROM-specific offset or a fixed Super Mario Bros. camera.

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

Next tutorial step:

Step 330) Compose a horizontal framebuffer viewport across two nametables
	Files:
		emulator/rendering/background_viewport.py
		tests/chapter_13_scrolling/test_330_compose_horizontal_framebuffer_viewport.py

	Behavior:
		Given two adjacent 256x240 background framebuffers and a horizontal viewport X,
		return a new 256x240 framebuffer containing the selected logical region.

		Examples:
			viewport X = 0   -> all pixels come from the left nametable
			viewport X = 200 -> 56 pixels from left, then 200 from right
			viewport X = 256 -> all pixels come from the right nametable

		Wrap the logical horizontal source coordinate across the combined 512-pixel
		background width.

	Goal:
		prove viewport selection and seam crossing as a pure framebuffer transformation
		before reading PPU memory or changing Console.

	Important:
		Return a new framebuffer; do not mutate either source framebuffer.
		Keep pygame outside emulator/rendering.
		Do not read PpuBus or PPU state in this step.
		Do not scroll the background opacity mask yet; that is the next focused step.

	After this:
		Step 331) Compose the opacity mask with the same horizontal viewport mapping.
		Step 332) Extract/render adjacent logical nametables from current PPU state.
		Step 333) Integrate scrolled framebuffer and mask into Console rendering.
		Step 334) VALIDATION: manually revisit Super Mario Bros. horizontal movement.

Phase map:
	- Phase 7: pure rendering pipeline plus manual pygame smoke runner
	- Phase 8 / Chapter 06: ROM startup preparation
	- Phase 9 / Chapter 07: controller $4016 behavior
	- Phase 10: manual main.py execution path
	- Phase 11 / Chapter 09: sprite rendering
	- Phase 12 / Chapter 10: performance and manual runtime
	- Phase 13 / Chapter 11: sprite 0 hit
	- Phase 14 / Chapter 12: cartridge nametable mirroring
	- Phase 15 / Chapter 13: PPU scrolling and background viewport

Controller phase outline:
	Controller state stores 8 buttons in NES read order:
		A, B, Select, Start, Up, Down, Left, Right

	CPU write $4016 controls strobe/latch behavior.
	CPU read $4016 returns one button bit at a time.
	Pygame keyboard input should only be connected after the pure controller
	protocol is tested.
---------------------------------------------
Future Notes:

	- Refine sprite 0 hit accuracy later:
		- exact OAM Y+1 behavior
		- PPUMASK rendering/left-edge rules
		- x=255 exception
		- exact dot timing
		- 8x16 sprites
	- Implement Sprite Overflow flag behavior later:
		- OAM memory
		- sprite evaluation per scanline
		- more than 8 sprites on a scanline
		- quirky NES hardware behavior
	- Add vertical and complete two-dimensional background viewport support after the
	  horizontal scrolling milestone is integrated and validated:
		- compose a 256x240 viewport across vertically adjacent top/bottom nametables
		- compose the background opacity mask with the identical vertical mapping
		- combine four logical nametables for viewports crossing X and Y boundaries
		- preserve PpuBus ownership of cartridge nametable mirroring
		- model coarse-Y row 29 wrapping and the special row 30/31 behavior explicitly
		- replace the simplified frame-level t + fine-X snapshot with timed v + fine-X
		  rendering state when dot-accurate scrolling is introduced
		- measure allocations and composition cost before optimizing framebuffer copies

	  References:
		- https://www.nesdev.org/wiki/PPU_scrolling
		- https://www.nesdev.org/wiki/PPU_scrolling#Wrapping_around
		- https://www.nesdev.org/wiki/PPU_scrolling#During_rendering
		- https://www.nesdev.org/wiki/PPU_nametables
