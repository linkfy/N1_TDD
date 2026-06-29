from emulator.cpu.cpu import CPU
from emulator.bus.cpu_bus import CpuBus
from emulator.memory.fake_rom import FakeROM


def test_lda_absolute_without_flags():
    """
    Implement LDA Absolute 0xAD opcode
    Fetch the value from a 16-bit value address in memory
    """
    
    # Current flow CPU Status: Reset -> Fetch -> Decode
    rom = FakeROM()
    
    # Reset Vector
    rom.write(0x7FFC, 0x00)
    rom.write(0x7FFD, 0x80)


    # LDA Absolute X
    rom.write(0x0000, 0xAD) # LDA Absolute opcode
    rom.write(0x0001, 0x34)
    rom.write(0x0002, 0x12) # Address => 0x1234


    bus = CpuBus(program_rom=rom)
    bus.write(0x1234, 0x42)
    cpu = CPU(bus)

    cpu.reset()
    cpu.step() # LDA should fetch_byte and put it on register A

    assert cpu.a == 0x42


def test_lda_absolute_sets_zero_flag():
    """
    Test LDA Absolute Zero flag ON
    """
     # Current flow CPU Status: Reset -> Fetch -> Decode
    rom = FakeROM()
    
    # Reset Vector
    rom.write(0x7FFC, 0x00)
    rom.write(0x7FFD, 0x80)


    # LDA Absolute X
    rom.write(0x0000, 0xAD) # LDA Absolute opcode
    rom.write(0x0001, 0x34)
    rom.write(0x0002, 0x12) # Address => 0x1234


    bus = CpuBus(program_rom=rom)
    bus.write(0x1234, 0x00) # Value set to 0
    cpu = CPU(bus)

    cpu.reset()
    cpu.step() # LDA should fetch_byte and put it on register A

    assert (cpu.p & (1 << 1)) != 0 # Flag Zero is set


def test_lda_absolute_clears_zero_flag():
    """
    Test LDA Absolute Zero flag ON
    """
     # Current flow CPU Status: Reset -> Fetch -> Decode
    rom = FakeROM()
    
    # Reset Vector
    rom.write(0x7FFC, 0x00)
    rom.write(0x7FFD, 0x80)


    # LDA Absolute X
    rom.write(0x0000, 0xAD) # LDA Absolute opcode
    rom.write(0x0001, 0x34)
    rom.write(0x0002, 0x12) # Address => 0x1234
    
    rom.write(0x0003, 0xAD) # LDA Absolute opcode
    rom.write(0x0004, 0x35)
    rom.write(0x0005, 0x12) # Address => 0x1235



    bus = CpuBus(program_rom=rom)
    bus.write(0x1234, 0x00) # Value set to 0
    bus.write(0x1235, 0x01) # Next value set to 1
    cpu = CPU(bus)

    cpu.reset()

    cpu.step() # Set Zero Flag
    assert (cpu.p & (1 << 1)) != 0 # Flag Zero is set

    cpu.step() # Should Unset Zero Flag
    assert (cpu.p & ( 1 << 7 )) == 0 # N = 0

# TODO: Define 
# def test_lda_absolute_sets_negative_flag():
# def test_lda_absolute_clears_negative_flag():
