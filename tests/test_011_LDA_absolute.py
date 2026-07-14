from emulator.cpu.cpu import CPU
from emulator.bus.cpu_bus import CpuBus
from emulator.memory.fake_rom import FakeROM


def test_lda_absolute_without_flags():
    """
    Implement LDA Absolute 0xAD opcode.

    LDA Absolute fetches a 16-bit address from ROM using little-endian
    order, then reads the value stored at that address in memory.

    Program:
    AD 34 12 -> LDA $1234
    """

    rom = FakeROM()

    # Reset Vector
    rom.write(0x7FFC, 0x00)
    rom.write(0x7FFD, 0x80)

    # LDA Absolute
    rom.write(0x0000, 0xAD)  # LDA Absolute opcode
    rom.write(0x0001, 0x34)  # Low byte
    rom.write(0x0002, 0x12)  # High byte => address 0x1234

    bus = CpuBus(program_rom=rom)
    bus.write(0x1234, 0x42)

    cpu = CPU(bus)

    cpu.reset()
    cpu.step()

    assert cpu.a == 0x42


def test_lda_absolute_sets_zero_flag():
    """
    Test LDA Absolute Zero flag ON.

    If the loaded value is 0x00, the Zero flag must be set.
    """

    rom = FakeROM()

    # Reset Vector
    rom.write(0x7FFC, 0x00)
    rom.write(0x7FFD, 0x80)

    # LDA Absolute
    rom.write(0x0000, 0xAD)
    rom.write(0x0001, 0x34)
    rom.write(0x0002, 0x12)  # Address => 0x1234

    bus = CpuBus(program_rom=rom)
    bus.write(0x1234, 0x00)  # Value set to 0

    cpu = CPU(bus)

    cpu.reset()
    cpu.step()

    assert cpu.a == 0x00
    assert (cpu.p & (1 << 1)) != 0  # Z flag set


def test_lda_absolute_clears_zero_flag():
    """
    Test LDA Absolute Zero flag OFF.

    This test runs two LDA Absolute instructions:

    1. First LDA loads 0x00, setting the Zero flag.
    2. Second LDA loads 0x01, clearing the Zero flag.

    This ensures that LDA can both set and clear Z.
    """

    rom = FakeROM()

    # Reset Vector
    rom.write(0x7FFC, 0x00)
    rom.write(0x7FFD, 0x80)

    # First instruction: LDA $1234
    rom.write(0x0000, 0xAD)
    rom.write(0x0001, 0x34)
    rom.write(0x0002, 0x12)

    # Second instruction: LDA $1235
    rom.write(0x0003, 0xAD)
    rom.write(0x0004, 0x35)
    rom.write(0x0005, 0x12)

    bus = CpuBus(program_rom=rom)
    bus.write(0x1234, 0x00)  # First value: should set Z
    bus.write(0x1235, 0x01)  # Second value: should clear Z

    cpu = CPU(bus)

    cpu.reset()

    cpu.step()
    assert cpu.a == 0x00
    assert (cpu.p & (1 << 1)) != 0  # Z flag set

    cpu.step()
    assert cpu.a == 0x01
    assert (cpu.p & (1 << 1)) == 0  # Z flag clear


def test_lda_absolute_sets_and_clears_negative_flag():
    """
    Test LDA Absolute Negative flag ON and OFF.

    The Negative flag is based on bit 7 of the loaded value:

    0x80 = 1000_0000 -> N flag set
    0x7F = 0111_1111 -> N flag clear
    """

    rom = FakeROM()

    # Reset Vector
    rom.write(0x7FFC, 0x00)
    rom.write(0x7FFD, 0x80)

    # First instruction: LDA $1234
    rom.write(0x0000, 0xAD)
    rom.write(0x0001, 0x34)
    rom.write(0x0002, 0x12)

    # Second instruction: LDA $1235
    rom.write(0x0003, 0xAD)
    rom.write(0x0004, 0x35)
    rom.write(0x0005, 0x12)

    bus = CpuBus(program_rom=rom)

    bus.write(0x1234, 0x80)  # 0x80 = 1000_0000
    bus.write(0x1235, 0x7F)  # 0x7F = 0111_1111

    cpu = CPU(bus)

    cpu.reset()

    cpu.step()
    assert cpu.a == 0x80
    assert (cpu.p & (1 << 7)) != 0  # N flag set

    cpu.step()
    assert cpu.a == 0x7F
    assert (cpu.p & (1 << 7)) == 0  # N flag clear
