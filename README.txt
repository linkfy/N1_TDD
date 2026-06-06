Phase 1) 
CPU:
- Declare Registers
- Flags
- Address Mode
- Instructions

Phase 2)
Memory Map:
- RAM
- PPU Registers dummy
- Cartridge dummy 

Phase 3)
iNES parser file parser .nes

Phase 4)
NROM mapper (No Bank Switch)

Phase 5)
PPU (Basic)

Phase 6)
Rendering


--

Steps:
Install pytest
Let's start by cpu, it is connected to cpu bus and internal ram. Let's create the first element of memory map: RAM <- BUS -> CPU

Declare basic folders: 
cpu/
  addressing_modes.py // Addressing modes 
  cpu.py 
  instructions.py 

memory/
  ram.py

bus/
  cpu_bus.py
