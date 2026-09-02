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
[x] Compose a 256x240 framebuffer viewport across two horizontal nametables
[x] Compose the matching scrolled background opacity mask
[x] Render one logical nametable framebuffer from a selected PPU base address
[x] Build one logical nametable opacity mask from a selected PPU base address
[x] Extract and compose the horizontal viewport framebuffer from current PPU state
[x] Extract and compose the matching horizontal viewport opacity mask
[x] Integrate the scrolled viewport into Console background/full-frame rendering
[x] Read and acknowledge the timed v/t/x scrolling plan
[x] Increment horizontal v with coarse-X/nametable wrapping
[x] Copy horizontal bits from t into v
[x] Apply horizontal increments and the dot-257 copy during PPU stepping
[x] Increment vertical v with fine-Y and rows 29-31 wrapping
[x] Copy vertical bits from t into v
[x] Apply vertical dot-256 increment and pre-render t-to-v copy
[x] Rewind horizontal v to account for the two prefetched tiles
[x] Record effective v + fine-X for each visible scanline
[x] Publish a complete 240-scanline frame and reset the current recording buffer
[x] Select the horizontal logical nametable pair for one scanline state
[x] Decode horizontal viewport X from one scanline state
[x] Compose each timed framebuffer row exactly once
[x] Use timed framebuffer data only when all 240 scanline states exist
[x] Compose opacity-mask rows from the identical scanline states
[x] Use timed opacity-mask data only when all 240 scanline states exist
[x] Use the scanline-aware opacity mask for sprite-zero-hit scheduling

Chapter 13 complete through Test 353. The previously proposed separate manual
validation lesson was removed by project decision; the successful local Super Mario
Bros. run and measured FPS regression are retained below as engineering evidence.

Phase 16 / Chapter 14)
Evidence-driven rendering performance:
[ ] Cache background opacity masks by exact immutable graphics inputs
[ ] Continue profiling before selecting another production optimization

--
Next Steps:

Goal:
Prioritize a working main.py/manual execution path for Mapper000/NROM ROMs while
preserving the linear pytest tutorial flow and avoiding later refactors.

Incremental test policy:
	Each numbered test is a permanent record of what the student learned at that step.
	Do not modify an older test so it expects a function, name, or behavior introduced
	by a later step.

	When new behavior replaces an old internal path, preserve earlier expectations in
	production code with the smallest clear compatibility mechanism: a default argument,
	an import alias, a wrapper, or a separate legacy-facing method.

	Add new expectations only in the new numbered test. Every earlier test must continue
	passing unchanged. If a new design cannot coexist with an old test, stop and
	reconsider the production API instead of rewriting the old lesson.

	Mandatory gate after every numbered step:

		uv run pytest

	Do not proceed to the next step until the complete suite passes. This test gate is
	part of every step and must not be represented as a separate roadmap step.

Immediate direction:
	Manual ROM execution now reaches visible background output, sprite rendering,
	keyboard input, sprite/background priority, paced NES-speed presentation, and
	sprite-0-hit timing behavior.

	The Super Mario Bros. manual checkpoint proves that horizontal nametable composition
	works, but one end-of-frame temp_vram_addr snapshot cannot represent the fixed status
	bar and moving gameplay area in the same frame.

	The tutorial will model timed v/t/x behavior, record the effective rendering address
	per visible scanline, and preserve the existing nametable/framebuffer renderers. Each
	output row will be composed once for both RGB pixels and the opacity mask.

	Historical implementation note:
	Timed scrolling was first validated in an isolated experiment/ppu-vt-scroll worktree.
	That temporary worktree guided the incremental Tests 338-353 and may be removed after
	chapter completion. Main production code and permanent numbered tests are now the
	canonical evidence; no runtime, test, or documentation dependency should retain a local
	worktree path.

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

	Performance checkpoint at Test 337:
	The current launcher is observed at approximately 50 FPS on the development machine,
	below the NTSC target of 60.0988 FPS. Preserve this measurement as a reminder during
	the upcoming timed-scrolling work. First make v/t/x behavior correct and keep every
	output row single-pass; then profile before choosing an optimization.

	Performance checkpoint at Step 353:
	Manual Super Mario Bros. observation fell from approximately 45 FPS to 35 FPS after
	changing sprite-zero-hit mask acquisition from the fixed one-nametable producer to the
	viewport-aware opacity-mask adapter. Record this as correlation from a one-line import
	change, not yet as a proven root cause.

	The likely mechanism is duplicate expensive work: Console prepares a viewport-aware
	mask for sprite-zero-hit scheduling and later prepares another viewport-aware mask for
	visual sprite priority. Each preparation may rebuild logical nametable masks and walk
	61,440 destination pixels. Chapter 13 correctness is now complete; profile call counts
	and time in an isolated performance worktree before designing shared frame artifacts or
	cache invalidation. Do not revert to the incorrect fixed mask merely to recover FPS.

	Performance experiment accepted for Chapter 14:
	A bounded content-addressed cache for source background opacity masks improved the
	manual Super Mario Bros. result by approximately 5-7 FPS, from about 35 FPS to roughly
	40-42 FPS. The experiment caches immutable tuple data by exact pattern-table and
	nametable bytes, then returns a fresh list to preserve the public mutable mask contract.

	This is evidence from the isolated performance worktree, not yet completed main-branch
	tutorial work. Step 354 will add the implementation and permanent tests on main before
	the optimization is considered integrated.

	Likely areas to measure later include repeated pattern-table decoding, repeated
	nametable rendering, framebuffer/mask row loops, and temporary allocations. Numba may
	be evaluated only as a measured experiment, not as the default solution. The current
	launcher uses PyPy, while Numba is generally a CPython-oriented runtime choice, so
	adopting it would require an explicit runtime/tooling decision.

	PyPy is a supported manual runtime target through explicit launcher files. Do not
	change the project's default Python interpreter yet; keep PyPy opt-in for manual
	runs.

	Pygame performance work belongs in manual/frontend helpers such as tools/ and
	main.py. It must not introduce pygame into emulator core modules.

	Expected-speed control belongs in main.py/manual runtime code. The emulator core
	should remain deterministic stepping/rendering logic and should not sleep.

Next tutorial step:

	Chapter 13 has no remaining numbered tutorial step. Test 353 completes the scrolling
	and viewport-mask milestone.

Step 354) Cache background opacity masks by exact graphics bytes
	Files:
		emulator/rendering/nametable_renderer.py
		tests/chapter_14_rendering_performance/test_354_cache_background_opaque_mask.py

	Behavior:
		Add a private @lru_cache(maxsize=8) helper keyed by the immutable pattern_table and
		nametable bytes already accepted by build_background_opaque_mask(). Build and store an
		immutable tuple[bool, ...] on a cache miss.

		Keep build_background_opaque_mask() as the public list[bool] API. It must return a fresh
		list copied from the cached tuple on every call so caller mutation cannot corrupt a
		future result.

	Goal:
		avoid repeating CHR decoding and 61,440-pixel source-mask construction when visual
		priority and sprite-zero-hit request masks from identical graphics bytes.

	Important:
		Cache by exact content, not PPU identity, frame number, or undocumented lifecycle.
		Changed pattern-table bytes or changed nametable bytes must always cause a cache miss.
		Keep the cached value immutable and the cache bounded to eight entries.
		Preserve all validation errors and the BackgroundOpaqueMask list[bool] contract.
		Clear the private cache at the start of cache-sensitive tests so hit/miss assertions
		remain deterministic and independent.

	Measured evidence:
		The isolated PyPy/manual Super Mario Bros. experiment improved approximately 5-7 FPS,
		from about 35 FPS to roughly 40-42 FPS, with scrolling, visual priority, and game
		progress still working.

	After this:
		Do not add another optimization until profiling identifies a new bottleneck and an
		isolated experiment demonstrates a reproducible benefit.

	Completed horizontal milestone:
		Step 332: address-aware framebuffer extraction       complete
		Step 333: address-aware opacity-mask extraction      complete
		Step 334: framebuffer horizontal viewport adapter    complete
		Step 335: opacity-mask horizontal viewport adapter   complete
		Step 336: Console visual/priority integration        complete
		Step 337: timed-scroll reading checkpoint            complete
		Steps 338-340: horizontal v/t timing                  complete
		Step 341: pure vertical v increment                   complete
		Steps 342-343: vertical copy and timing               complete
		Step 344: pure two-tile prefetch rewind helper       complete
		Step 345: effective scanline-state recording         complete
		Step 346: publish/reset completed scanline states    complete
		Step 347: pure scanline logical-pair selection       complete
		Step 348: pure scanline viewport-X decoding          complete
		Step 349: row-limited framebuffer composition        complete
		Step 350: timed framebuffer/fallback selection       complete
		Step 351: matching opacity-mask row composition      complete
		Step 352: timed opacity-mask/fallback selection      complete
		Step 353: scanline-aware sprite-zero-hit mask        complete

	Completed Phase 15 / Chapter 13 implementation record:

	Current main-branch state:
		Steps through 353 are complete. PPU owns an immutable
		completed_scanline_scroll_states tuple containing either exactly 240
		BackgroundScanlineState values or no values. Existing frame-level viewport helpers
		must remain available as fallback behavior throughout the migration.

	Canonical timed-rendering functions in
		emulator/rendering/ppu_background_renderer.py:

			_scanline_horizontal_pair
			_scanline_viewport_x
			_timed_scanlines_to_framebuffer
			_timed_scanlines_to_opaque_mask
			ppu_background_viewport_to_framebuffer
			ppu_background_viewport_to_opaque_mask

		The temporary reference worktree is no longer required. Preserve these contracts and
		the numbered tests on main as the durable implementation record.

	Step 347 contract — logical pair for one scanline:
		Input: one BackgroundScanlineState.
		Read vertical nametable bit 11 from state.vram_addr.
		Return ($2000, $2400) for bit 0 or ($2800, $2C00) for bit 1.
		Do not inspect bit 10 for pair selection. Do not read PpuBus or render pixels.

	Step 348 contract — horizontal viewport X for one scanline:
		Input: one BackgroundScanlineState.
		Decode coarse X and horizontal nametable from state.vram_addr and combine them with
		state.fine_x:

			viewport_x = nametable_x * 256 + coarse_x * 8 + fine_x

		The packed v layout matches t, so the existing viewport decoder may be reused. Do
		not apply another two-tile rewind; Step 345 already stored the compensated address.

	Step 349 contract — timed framebuffer rows:
		Input: a PPU with 240 completed states.
		Create one 256x240 result framebuffer.
		For each screen_y, use completed state[screen_y], the Step 347 pair, and Step 348 X.
		Cache rendered left/right source framebuffers by left_base so repeated scanlines do
		not repeatedly decode the same nametables and pattern data.
		Copy only that row's 256 pixels directly into the result. Do not call the full
		256x240 viewport compositor once per scanline or band. Across the frame, every
		output pixel must be assigned exactly once.
		For this horizontal milestone, source Y remains screen_y. Full vertical source-row
		selection remains future work.

	Step 350 contract — timed framebuffer selection with fallback:
		At the start of ppu_background_viewport_to_framebuffer(ppu), use the timed row helper
		only when len(ppu.completed_scanline_scroll_states) == 240. Otherwise execute the
		existing temp_vram_addr + fine_x viewport path unchanged. Do not remove or rename the
		one-nametable helpers or Console compatibility behavior.

	Step 351 contract — matching opacity-mask rows:
		Mirror Step 349 using BackgroundOpaqueMask source pairs and one Boolean result list
		of 256 * 240 entries. Use the same state index, logical pair, viewport X, wrap rule,
		and source X for every pixel. Cache mask pairs by left_base. Reject input whose length
		is not 240. Keep ppu_background_viewport_to_opaque_mask(ppu) unchanged in this step.

		Critical invariant:

			framebuffer coordinate mapping == opacity-mask coordinate mapping

	Step 352 contract — timed opacity-mask selection with fallback:
		At the start of ppu_background_viewport_to_opaque_mask(ppu), use the timed mask helper
		only when len(ppu.completed_scanline_scroll_states) == 240. Return immediately from
		that branch. For every other length, preserve the existing temp_vram_addr + fine_x
		mask path unchanged.

	Step 353 contract — sprite-zero-hit uses the same mask:
		This final wiring was completed and tested on main after the timed-rendering reference.
		ppu_sprite_zero_hit_position(ppu) must obtain the viewport-aware opacity mask used
		by full-frame rendering. Preserve the older local helper name through an import alias
		if required by historical tests, following the same compatibility pattern already
		used in emulator/console.py. Do not calculate nametable addresses in sprite-zero-hit
		code. Keep find_sprite_zero_hit_position() pure and unchanged.

	Shared constraints for follow-up performance experiments:
		Do not modify older numbered tests.
		Run `uv run pytest` before proceeding.
		Keep pygame outside emulator core modules.
		Keep PpuBus responsible for cartridge nametable mirroring.
		Keep timed row composition single-pass and bounded.
		Use only stable reference URLs or links already verified/provided in this repository.

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
	- Phase 16 / Chapter 14: evidence-driven rendering performance

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
	- Complete visible vertical viewport composition after the timed scrolling milestone
	  is integrated and validated:
		- compose a 256x240 viewport across vertically adjacent top/bottom nametables
		- compose the background opacity mask with the identical vertical mapping
		- combine four logical nametables for viewports crossing X and Y boundaries
		- preserve PpuBus ownership of cartridge nametable mirroring
		- use the timed per-scanline v state to select the source Y row
		- measure allocations and composition cost before optimizing framebuffer copies

	  References:
		- https://www.nesdev.org/wiki/PPU_scrolling
		- https://www.nesdev.org/wiki/PPU_scrolling#Wrapping_around
		- https://www.nesdev.org/wiki/PPU_scrolling#During_rendering
		- https://www.nesdev.org/wiki/PPU_nametables
