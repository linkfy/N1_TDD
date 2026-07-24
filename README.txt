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

[] Phase 3)
Debug trace
iNES parser file parser .nes
	
Phase 4)
NROM mapper (No Bank Switch)

Phase 5)
PPU Registers dummy
PPU (Basic)

Phase 6)
Rendering


--
Next Steps:
1) PPU Object
Implement:
- PPU
	- write_register(addr, value)
	- read_register(addr)
2) CpuBus routing
Roite $2000-$3FFF -> Mirrors $2000-$2007 PPU Registers
CpuBus.write($2000, value) -> ppu.write_register($2000, value)
CpuBus.read(addr) -> ppu.read_register(addr)

