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

Add a mapper factory helper emulator/cartridge/mapper_factory.py

def create_mapper(cartridge):
	if cartridge.mapper == 0 return Mapper000(cartridge.prg_rom, cartridge.chr_rom)

Add Optional CpuBus(cartridge=cartridge) -> in CpuBus.__post__init create mapper if cartridge exists.
Then Reads $8000-$FFF -> if mapper exists: return ampper.read_prg(addr) else: old behaviour
