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
    rom.write(0x0000, 0xAE) # LDA Absolute opcode
    rom.write(0x0001, 0x34)
    rom.write(0x0002, 0x12) # Address => 0x1234


    bus = CpuBus(program_rom=rom)
    bus.write(0x1234, 0x42)
    cpu = CPU(bus)

    cpu.reset()
    cpu.step() # LDA should fetch_byte and put it on register A

    assert cpu.a == 0x42
    # TODO: Implement opcode 0xAD
    # it should: fetch_word() and save it to cpu.a
    # other tests: ensure flags


