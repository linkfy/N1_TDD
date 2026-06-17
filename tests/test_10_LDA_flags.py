from emulator.cpu.cpu import CPU
from emulator.bus.cpu_bus import CpuBus
from emulator.memory.fake_rom import FakeROM

def test_lda_clears_zero_flag():
    """Now it's time configure LDA flags
    Ensure that zero flag is unset (clear)

    If result == 0 -> Flag Zero is set 

    7  bit  0
    ---- ----
    NV1B DIZC
    |||| ||||
    |||| |||+- Carry
    |||| ||+-- Zero
    |||| |+--- Interrupt Disable
    |||| +---- Decimal
    |||+------ (No CPU effect; see: the B flag)
    ||+------- (No CPU effect; always pushed as 1)
    |+-------- Overflow
    +--------- Negative
    
    Pseudocode:
    if LDA:
      if self.a == 0:
        set flag Z
     else: 
        clear flag Z

    """
    rom = FakeROM()
    
    rom.write(0x7FFC, 0x00)
    rom.write(0x7FFD, 0x80)

    rom.write(0x0000, 0xA9)
    rom.write(0x0001, 0x42)

    bus = CpuBus(program_rom=rom)
    cpu = CPU(bus)

    cpu.reset()
    cpu.step() 

    assert cpu.a == 0x42
    assert (cpu.p & (1 << 1)) == 0 # Flag Zero is clear (0)


def test_lda_sets_zero_flag():
    """
    Ensure that zero flag is set

    if self.a == 0 -> set flag Z else Z is cleared
    Pseudocode:
    if LDA:
     if self.a == 0:
        set flag Z
     else: 
        clear flag Z

    """
    rom = FakeROM()
    
    rom.write(0x7FFC, 0x00)
    rom.write(0x7FFD, 0x80)

    rom.write(0x0000, 0xA9)
    rom.write(0x0001, 0x00)

    bus = CpuBus(program_rom=rom)
    cpu = CPU(bus)

    cpu.reset()
    cpu.step() 

    assert cpu.a == 0x00
    assert (cpu.p & (1 << 1)) != 0 # Flag Zero is set

def test_lda_sets_negative_flag():
    assert 0 == 1, "Test should be implemented"
