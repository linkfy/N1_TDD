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
cartridge/cartridge.py -> represents NES cartirdfe data -> Create Cartirdge(prg_rom, chr_rom, mapper_number):
	- it will have a class method -> from_ines_bytes(cls, data: bytes) -> "Cartirdge" (that uses parse_ines_rom(data) inside)
cartridge/mapper000.py -> maps cartridge RPG ROM into CPU address space 
