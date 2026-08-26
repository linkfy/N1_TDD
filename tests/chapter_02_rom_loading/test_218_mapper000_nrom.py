"""
Add Mapper000 / NROM PRG ROM mapping.

File to create:
    emulator/cartridge/mapper000.py

What is Mapper000?
Mapper000 is the simplest NES cartridge mapper. It is also called NROM.

At this stage, we only test CPU reads from PRG ROM:

    read_prg(addr: int) -> int

Mapper000 should already store both:

    prg_rom: bytes
    chr_rom: bytes
----
Note: chr_rom will be used in the next test
We are not testing PPU CHR reads, nametable mirroring, mapper writes, or bank
switching in this file yet.
----
Why this step exists:
The CPU does not read PRG ROM using offset 0 directly. It reads CPU addresses in
the range:

    $8000-$FFFF

The mapper translates those CPU addresses into offsets inside PRG ROM bytes.

Mapper000 rules:

    NROM-128: 16KB PRG ROM
        $8000-$BFFF -> PRG offset $0000-$3FFF
        $C000-$FFFF -> mirror of the same 16KB

    NROM-256: 32KB PRG ROM
        $8000-$FFFF -> PRG offset $0000-$7FFF

Common mistake:
Do not put this address translation in Cartridge. Cartridge stores ROM data and
mapper number. Mapper000 performs the hardware address mapping.
"""

import dataclasses
from pathlib import Path

import pytest

from emulator.cartridge.mapper000 import (
    CHR_ROM_SIZE,
    Mapper000,
    NROM_128_SIZE,
    NROM_256_SIZE,
    PRG_ROM_END,
    PRG_ROM_START,
)


def make_mapper(prg_rom: bytes) -> Mapper000:
    """Create Mapper000 with placeholder CHR ROM for PRG-focused tests."""
    chr_rom = bytes([0x00]) * CHR_ROM_SIZE
    return Mapper000(prg_rom=prg_rom, chr_rom=chr_rom)


def test_mapper000_file_and_constants_exist():
    """
    Step 1: define Mapper000 constants.

    Required constants:
        PRG_ROM_START = 0x8000
            First CPU address where cartridge PRG ROM is visible.

        PRG_ROM_END = 0xFFFF
            Last CPU address in the PRG ROM area.

        NROM_128_SIZE = 16 * 1024
            16KB PRG ROM case. This must be mirrored into $C000-$FFFF.

        NROM_256_SIZE = 32 * 1024
            32KB PRG ROM case. This maps directly across $8000-$FFFF.

    Why constants:
    Mapper code is address-heavy. Constants keep the mapping rules readable and
    prevent magic numbers from hiding the hardware model.
    """
    assert Path("emulator/cartridge/mapper000.py").exists()
    assert PRG_ROM_START == 0x8000
    assert PRG_ROM_END == 0xFFFF
    assert NROM_128_SIZE == 16 * 1024
    assert NROM_256_SIZE == 32 * 1024


def test_mapper000_class_exists_and_stores_prg_and_chr_rom():
    """
    Step 2: define Mapper000.

    Mapper000 should store PRG ROM and CHR ROM bytes.

    At this tutorial step, read_prg is the only behavior we need because the CPU
    bus will eventually ask the mapper how to read addresses $8000-$FFFF.

    CHR ROM is included now because the next test will add read_chr(addr) for
    future PPU pattern-table reads.

    Later tutorial steps may append optional mapper metadata while preserving these
    original fields and their constructor order.
    """
    assert dataclasses.is_dataclass(Mapper000)
    original_fields = ["prg_rom", "chr_rom"]
    field_names = list(Mapper000.__dataclass_fields__)

    assert field_names[: len(original_fields)] == original_fields
    assert hasattr(Mapper000, "read_prg")
    assert callable(Mapper000.read_prg)


def test_mapper000_16kb_prg_reads_lower_bank():
    """
    Objective:
    With 16KB PRG ROM, $8000 maps to PRG offset $0000.
    """
    prg_rom = bytes([0xAA]) + bytes([0x00]) * (NROM_128_SIZE - 1)
    mapper = make_mapper(prg_rom)

    assert mapper.read_prg(0x8000) == 0xAA


def test_mapper000_16kb_prg_mirrors_upper_bank():
    """
    Objective:
    With 16KB PRG ROM, $C000-$FFFF mirrors $8000-$BFFF.

    That means:
        $8000 and $C000 both map to PRG offset $0000.
    """
    prg_rom = bytes([0xAA]) + bytes([0x00]) * (NROM_128_SIZE - 1)
    mapper = make_mapper(prg_rom)

    assert mapper.read_prg(0x8000) == 0xAA
    assert mapper.read_prg(0xC000) == 0xAA


def test_mapper000_16kb_prg_reads_last_mirrored_byte():
    """
    Objective:
    With 16KB PRG ROM, $FFFF maps to PRG offset $3FFF.
    """
    prg_rom = bytes([0x00]) * (NROM_128_SIZE - 1) + bytes([0xEF])
    mapper = make_mapper(prg_rom)

    assert mapper.read_prg(0xBFFF) == 0xEF
    assert mapper.read_prg(0xFFFF) == 0xEF


def test_mapper000_32kb_prg_maps_directly():
    """
    Objective:
    With 32KB PRG ROM, $8000-$FFFF maps directly to offsets $0000-$7FFF.
    """
    prg_rom = bytearray(NROM_256_SIZE)
    prg_rom[0x0000] = 0x11
    prg_rom[0x4000] = 0x22
    prg_rom[0x7FFF] = 0x33
    mapper = make_mapper(bytes(prg_rom))

    assert mapper.read_prg(0x8000) == 0x11
    assert mapper.read_prg(0xC000) == 0x22
    assert mapper.read_prg(0xFFFF) == 0x33


def test_mapper000_rejects_addresses_outside_prg_rom_range():
    """
    Objective:
    Mapper000 should only answer CPU PRG ROM reads in $8000-$FFFF.
    """
    mapper = make_mapper(bytes([0x00]) * NROM_128_SIZE)

    with pytest.raises(ValueError, match="Address out of PRG ROM range"):
        mapper.read_prg(0x7FFF)


def test_mapper000_rejects_unsupported_prg_rom_size():
    """
    Objective:
    Mapper000 supports only NROM-128 and NROM-256 PRG sizes.
    """
    mapper = make_mapper(bytes([0x00]) * 123)

    with pytest.raises(ValueError, match="Mapper000 supports only 16KB or 32KB PRG ROM"):
        mapper.read_prg(0x8000)
