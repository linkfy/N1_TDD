"""
At this point we have a MemoryDevice Abstract Class

It has the methods that we need to read+write on RAM and also on Fake ROMs

Let's create a FakeROM device to test it

The CpuBus will be responsible for mapping CPU addresses
to the appropriate memory device.
"""

from pathlib import Path
from emulator.memory.memory_device import MemoryDevice

def test_program_rom_class_exists():
    """
    We are going to create a Fake ROM for testing purposes
    It does not have any logic about how real cartridges work
    """
    assert Path("emulator/memory/fake_rom.py").exists()

def test_fake_rom_uses_memory_device_abstract_class():
    """
    Create a new FakeROM class inside fake_rom.py
    Ensure that it uses our abstract class MemoryDevice
    The methods read/write can be void on this test, just declare it
    """

    from emulator.memory.fake_rom import FakeROM

    assert FakeROM is not None

    rom = FakeROM()
    assert isinstance(rom, MemoryDevice)

def test_fake_rom_has_0x8000_bytes():
    """
    The CPU address range $8000-$FFFF is commonly used for PRG ROM.

    Look at: https://en.wikibooks.org/wiki/NES_Programming/Memory_Map
    NES has 2 Possible ROM Addresses 0x8000 and 0xC000

    Each one of 0x4000 Size, then the max size is 0x8000 [0x0000-0x7FFF]
    Lets implement a _data = bytearray(0x8000) inside our Fake ROM

    """

    from emulator.memory.fake_rom import FakeROM
    rom = FakeROM()
    assert hasattr(rom, "_data")
    assert isinstance(rom._data, bytearray)
    assert len(rom._data) == 0x8000

def test_write_read_fake_rom():
    """
    Remember: a real ROM will never implement Write methods,
    Our Fake ROM is for testing purposes and that's why we implement write
    """
    from emulator.memory.fake_rom import FakeROM
    fake_rom = FakeROM()

    for addr in range(0x0, 0x8000):
        test_value = addr & 0xFF

        fake_rom.write(addr, test_value)

        assert fake_rom.read(addr) == test_value
