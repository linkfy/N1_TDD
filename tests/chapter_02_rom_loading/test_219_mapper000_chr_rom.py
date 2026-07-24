"""
Add Mapper000 CHR ROM reads.

File already created:
    emulator/cartridge/mapper000.py

New behavior to add:
    Mapper000.read_chr(addr: int) -> int

Why this step exists:
Mapper000/NROM cartridges contain two important ROM areas:

    PRG ROM
        Program bytes read by the CPU through CPU addresses $8000-$FFFF.

    CHR ROM
        Graphics pattern bytes that will be read by the PPU through PPU pattern
        table addresses $0000-$1FFF.

We do NOT implement the PPU yet.

But it is useful to stabilize the Mapper000 data shape now:

    Mapper000(prg_rom, chr_rom)

That way, when the PPU exists later, it can ask the mapper for CHR bytes without
changing the mapper constructor or rewriting cartridge wiring.

Pseudocode for the new constants:

    CHR_ROM_START = 0x0000
    CHR_ROM_END = 0x1FFF
    CHR_ROM_SIZE = 8 * 1024

Pseudocode for read_chr:

    def read_chr(self, addr):
        if addr is outside $0000-$1FFF:
            raise ValueError

        if chr_rom is not exactly 8KB:
            raise ValueError

        offset = addr - CHR_ROM_START
        return chr_rom[offset]

Mapper000 CHR rules for this stage:
    - valid CHR address range is $0000-$1FFF
    - CHR ROM size is 8KB
    - read_chr($0000) returns chr_rom[0]
    - read_chr($1FFF) returns chr_rom[8191]

Common mistake:
Do not confuse CPU PRG address range with PPU CHR address range.

    CPU PRG range: $8000-$FFFF
    PPU CHR range: $0000-$1FFF
"""

import pytest

from emulator.cartridge.mapper000 import (
    CHR_ROM_END,
    CHR_ROM_SIZE,
    CHR_ROM_START,
    Mapper000,
    NROM_128_SIZE,
)


def make_mapper_with_chr(chr_rom: bytes) -> Mapper000:
    prg_rom = bytes([0x00]) * NROM_128_SIZE
    return Mapper000(prg_rom=prg_rom, chr_rom=chr_rom)


def test_mapper000_chr_constants_exist():
    """
    Objective:
    Define constants for the PPU CHR ROM address range.

    These are PPU-side addresses, not CPU-side addresses.
    """
    assert CHR_ROM_START == 0x0000
    assert CHR_ROM_END == 0x1FFF
    assert CHR_ROM_SIZE == 8 * 1024


def test_mapper000_stores_chr_rom_bytes():
    """
    Objective:
    Mapper000 stores CHR ROM bytes next to PRG ROM bytes.

    We are not using the PPU yet, but the mapper now has the data the PPU will
    eventually need.
    """
    chr_rom = bytes([0xAA]) * CHR_ROM_SIZE
    mapper = make_mapper_with_chr(chr_rom)

    assert mapper.chr_rom == chr_rom


def test_mapper000_read_chr_reads_first_pattern_table_byte():
    """
    Objective:
    PPU address $0000 maps to CHR ROM offset 0.
    """
    chr_rom = bytes([0xAB]) + bytes([0x00]) * (CHR_ROM_SIZE - 1)
    mapper = make_mapper_with_chr(chr_rom)

    assert mapper.read_chr(0x0000) == 0xAB


def test_mapper000_read_chr_reads_last_pattern_table_byte():
    """
    Objective:
    PPU address $1FFF maps to CHR ROM offset 8191.
    """
    chr_rom = bytes([0x00]) * (CHR_ROM_SIZE - 1) + bytes([0xEF])
    mapper = make_mapper_with_chr(chr_rom)

    assert mapper.read_chr(0x1FFF) == 0xEF


def test_mapper000_read_chr_rejects_addresses_outside_chr_range():
    """
    Objective:
    read_chr should only answer PPU pattern-table addresses $0000-$1FFF.
    """
    chr_rom = bytes([0x00]) * CHR_ROM_SIZE
    mapper = make_mapper_with_chr(chr_rom)

    with pytest.raises(ValueError, match="Address out of CHR ROM range"):
        mapper.read_chr(0x2000)


def test_mapper000_read_chr_rejects_wrong_chr_rom_size():
    """
    Objective:
    For this stage, Mapper000 expects exactly 8KB of CHR ROM.

    Later, cartridges with zero CHR ROM banks may use CHR RAM instead, but that
    is a future feature and should not be hidden in this first implementation.
    """
    mapper = make_mapper_with_chr(bytes([0x00]) * 123)

    with pytest.raises(ValueError, match="Mapper000 expects 8KB CHR ROM"):
        mapper.read_chr(0x0000)
