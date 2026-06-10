
"""
At this point we need both RAM and ROM-like devices to test
the CPU memory map.

RAM supports both read and write operations.

A real ROM would only allow reads. However, for testing purposes,
we need a memory device that can be populated with arbitrary data.

For that reason we will create a FakeROM. Despite its name, this
device is writable so tests can easily load instructions and data.

Before implementing FakeROM, we will introduce a common abstract
base class that defines the interface shared by all memory devices.

The CpuBus will be responsible for mapping CPU addresses
to the appropriate memory device.
"""

from inspect import signature
from pathlib import Path

from emulator.memory.ram import RAM

def test_memory_abstract_class_exists():
    assert Path("emulator/memory/memory_device.py").exists()

def test_memory_device_has_read_write_methods():
    """You should create a Memory Device abstract class with read and write methods"""

    from emulator.memory.memory_device import MemoryDevice
    abstract_methods = MemoryDevice.__abstractmethods__

    assert "read" in abstract_methods
    assert "write" in abstract_methods

def test_memory_read_has_corrrect_parameters():
    """Read should have:
        read(self, addr:int)
    """
    
    from emulator.memory.memory_device import MemoryDevice
    params = signature(MemoryDevice.read).parameters
    assert "self" in params
    assert "addr" in params
    assert len(params) == 2

def test_memory_write_has_corrrect_parameters():
    """Write should have:
        write(self, addr:int, value:int)
    """
 
    from emulator.memory.memory_device import MemoryDevice
    params = signature(MemoryDevice.write).parameters
    assert "self" in params
    assert "addr" in params
    assert "value" in params 
    assert len(params) == 3

def test_ram_uses_memory_device_abstract_class():
    """
    Now our ram should use the new abstract class Memory Device
    """

    from emulator.memory.memory_device import MemoryDevice
    ram = RAM()
    assert isinstance(ram, MemoryDevice)


