"""This test ensures that CpuBus exists and
proceeds to read and write to ram addresses

Focus: 
- Create CpuBus with RAM initialized
- Create Read/Write functions
- Include Support for Ram addresses

https://www.nesdev.org/wiki/CPU_memory_map

"""
import pytest
from emulator.bus.cpu_bus import CpuBus
from emulator.memory.ram import RAM

def test_cpu_buss_class_exists():
    assert CpuBus is not None

def test_create_ram_instance():
    cpu_bus = CpuBus()

    assert isinstance(cpu_bus, CpuBus)

def test_cpu_bus_contains_ram_instance():
    cpu_bus = CpuBus()

    assert hasattr(cpu_bus, "ram")
    assert isinstance(cpu_bus.ram, RAM)


def test_cpu_bus_reads_and_writes_internal_ram():
    bus = CpuBus()
    bus.write(0x0000, 0x42)

    assert bus.read(0x0000) == 0x42
    
def test_cpu_bus_reads_and_writes_internal_ram_mirrors():
    bus = CpuBus()

    mirrors = [0x800, 0x1000, 0x1800]
    test_addresses = [0x0, 0x1, 0x42, 0x7FF]
    # Write different values in mirror address
    value = 0
    for base_address in mirrors:
        for address in test_addresses:
            bus.write(base_address + address, value & 0xFF)
            assert bus.read(address) == value & 0xFF
            value+=1
    
def test_cpu_bus_rejects_invalid_addresses():
    """Addresses should be unsigned 16 bits"""
    bus = CpuBus()

    invalid_addresses = [
        -1,
        0x10000,
        0x20000,
    ]

    for addr in invalid_addresses:
        with pytest.raises(ValueError):
            bus.write(addr, 0x42)


def test_cpu_bus_rejects_invalid_values():
    """Values should be unsigned 8 bits"""
    bus = CpuBus()

    invalid_values = [
        -1,
        0x100,
        0xFFFF,
    ]

    for value in invalid_values:
        with pytest.raises(ValueError):
            bus.write(0x0000, value)
