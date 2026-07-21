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

Next steps:
memory/rom.py -> genery byte addressable read-only memory
cartridge/ines.py -> parses .nes/iNES file format 
cartridge/cartridge.py -> represents NES cartirdfe data 
cartridge/mapper000.py -> maps cartridge RPG ROM into CPU address space 
