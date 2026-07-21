"""
Add a real read-only ROM memory device.

File to create:
    emulator/memory/rom.py

Class to implement:
    ROM

Why this step exists:
Before parsing iNES files, we need a simple memory object that can hold raw ROM
bytes and expose read-only access.

Important distinction:
    FakeROM is writable because tests need to easily place bytes in memory.
    ROM is read-only because real cartridge ROM data should not be modified by
    CPU writes.

How this prepares us for iNES:
An iNES file is not itself just ROM bytes. It contains:
    - a 16-byte header
    - optional trainer data
    - PRG ROM bytes for the CPU
    - CHR ROM bytes for the PPU

Later, the iNES loader will extract PRG ROM bytes from the .nes file. Those raw
PRG bytes can then be stored in a ROM object or cartridge object and mapped into
CPU address space.

Design rule:
    ROM should only know how to read bytes.
    ROM should not know about iNES headers, mappers, CPU addresses, or PPU.

Expected implementation shape:

    from dataclasses import dataclass

    from emulator.memory.memory_device import MemoryDevice


    @dataclass
    class ROM(MemoryDevice):
        _data: bytes

        def write(self, addr: int, value: int) -> None:
            raise ValueError("Cannot write to ROM")

        def read(self, addr: int) -> int:
            return self._data[addr]
"""

import inspect
from pathlib import Path

import pytest

from emulator.memory.memory_device import MemoryDevice
from emulator.memory.rom import ROM


def test_rom_file_exists_inside_memory_package():
    """
    Objective:
    Create emulator/memory/rom.py.

    Why here:
    ROM is a generic memory device, like RAM and FakeROM. It should not live in
    the cartridge parser because it does not understand the iNES file format.
    """
    assert Path("emulator/memory/rom.py").exists()


def test_rom_is_a_memory_device():
    """
    Objective:
    ROM should implement the same MemoryDevice interface as RAM and FakeROM.

    This lets other emulator components depend on read/write behavior without
    caring whether the device is RAM, FakeROM, or ROM.
    """
    assert issubclass(ROM, MemoryDevice)


def test_rom_can_be_created_with_bytes_data():
    """Objective: ROM stores immutable bytes passed at construction time."""
    rom = ROM(bytes([0xA9, 0x42, 0xEA]))

    assert rom._data == bytes([0xA9, 0x42, 0xEA])


def test_rom_read_returns_byte_at_address():
    """
    Objective:
    ROM.read(addr) returns the byte stored at that offset.

    For PRG ROM later, mapper logic will translate CPU address $8000-$FFFF into
    a ROM offset. ROM itself only receives the final offset.
    """
    rom = ROM(bytes([0xA9, 0x42, 0xEA]))

    assert rom.read(0) == 0xA9
    assert rom.read(1) == 0x42
    assert rom.read(2) == 0xEA


def test_rom_write_is_rejected():
    """
    Objective:
    A real ROM device is read-only.

    CPU writes should not mutate ROM bytes. Later, cartridge mapper behavior can
    decide whether writes mean mapper control registers, but raw ROM data should
    stay immutable.
    """
    rom = ROM(bytes([0xA9, 0x42, 0xEA]))

    with pytest.raises(ValueError, match="Cannot write to ROM"):
        rom.write(0, 0x00)


def test_failed_rom_write_does_not_change_data():
    """Objective: rejected writes must leave ROM contents unchanged."""
    rom = ROM(bytes([0xA9, 0x42, 0xEA]))

    with pytest.raises(ValueError):
        rom.write(1, 0x99)

    assert rom.read(1) == 0x42


def test_rom_exposes_read_and_write_methods_with_memory_device_shape():
    """
    Objective:
    ROM should provide the same method names/signatures as MemoryDevice.
    """
    assert list(inspect.signature(ROM.read).parameters) == ["self", "addr"]
    assert list(inspect.signature(ROM.write).parameters) == ["self", "addr", "value"]
