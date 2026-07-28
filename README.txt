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
PPUADDR / PPUDATA write path:

Goal:
Allow CPU writes to PPU memory through PPU registers.

Architecture direction:
	CPU has CpuBus
	CpuBus has CPU RAM, PPU, and cartridge PRG path
	PPU has PpuBus
	PpuBus owns/routes PPU-side memory access

Important dependency direction:
	PPU -> PpuBus -> VRAM / mapper CHR later

Do not use:
	PPU -> VRAM -> PpuBus

Reason:
	PPU should talk to a stable PPU-address-space boundary.
	Later CHR ROM, nametable mirroring, and palette RAM can be added inside
	PpuBus without changing PPUDATA register behavior.

Testing rule:
	Do not update old tests such as test_224 now.
	Add new PPU fields incrementally only when a new step requires them.
	This keeps the student path linear and avoids unnecessary old-test churn.

Incremental path:

Step 239) PPUADDR internal address latch
	File:
		emulator/ppu/ppu.py

	Add state:
		vram_addr
		addr_latch

	Behavior:
		first write to $2006 sets high byte
		second write to $2006 sets low byte

	Pseudocode:
		if not addr_latch:
			vram_addr = (value & 0x3F) << 8
			addr_latch = True
		else:
			vram_addr = (vram_addr & 0x3F00) | value
			addr_latch = False

Step 240) PPUSTATUS read resets address latch
	File:
		emulator/ppu/ppu.py

	Behavior:
		read_register($2002)
			returns old status
			clears VBLANK_STARTED
			resets addr_latch = False

	Reason:
		Real PPUSTATUS reads reset the shared $2005/$2006 write latch.

Step 241) PPUDATA write through PpuBus
	File:
		emulator/ppu/ppu.py

	Behavior:
		write_register($2007, value)
			ppu_bus.write(vram_addr, value)
			vram_addr = (vram_addr + 1) & 0x3FFF
			data = value

Important registers:
$2006 PPUADDR
	- first write sets high byte of internal PPU address
	- second write sets low byte of internal PPU address

$2007 PPUDATA
	- writes value to current PPU memory address
	- then increments internal PPU address

Required new PPU state:
	vram_addr
	addr_latch
	ppu_bus

Basic behavior:
	write_register($2006, high)
	write_register($2006, low)
	write_register($2007, value)

Example:
	write $20 to $2006
	write $00 to $2006
	write $AA to $2007

Result:
	PPU memory[$2000] == $AA

Important:
	Keep this simple first.
	Do not implement full nametable mirroring, palette mirroring, rendering,
	or PPUDATA read buffering yet.

After that:
	- PPU memory map
	- Decode one CHR tile
	- Render one pattern table as debug image
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
