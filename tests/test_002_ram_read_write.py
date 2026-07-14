"""
RAM should only provide raw byte storage.

Address mirroring and memory mapping are responsibilities
of the CpuBus, not the RAM itself.

Focus: Create read/write to a Ram class
"""

from emulator.memory.ram import RAM

def test_ram_class_exists():
    assert RAM is not None

def test_create_ram_instance():
    ram = RAM()

    assert isinstance(ram, RAM)

def test_ram_has_2kb_capacity():
    ram = RAM()

    assert len(ram._data) == 2048


def test_write_read_ram():
    ram = RAM()

    for i in range(0x0, 0x800):
        test_value = i & 0xFF

        ram.write(i, test_value)

        assert ram.read(i) == test_value
