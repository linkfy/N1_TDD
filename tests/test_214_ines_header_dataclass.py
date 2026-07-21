"""
Create the INesHeader data class.

Class to implement:
    INesHeader

Why this class exists:
The first 16 bytes of an iNES file are the header. The header does not contain
CPU instructions. It contains metadata that tells the emulator how to interpret
the rest of the file.

Required fields:
    prg_rom_banks: int
        Number of 16KB PRG ROM banks. PRG ROM is what the CPU executes/reads.

    chr_rom_banks: int
        Number of 8KB CHR ROM banks. CHR ROM is graphics pattern data for the
        PPU later.

    mapper_number: int
        Identifies which mapper/hardware layout the cartridge uses. For the next
        stage, mapper 0 / NROM is the first one we will support.

    has_trainer: bool
        True when the file contains an optional 512-byte trainer after the
        header. If present, ROM extraction must skip it.

    flags_6: int
        Raw header byte 6. It stores mirroring/trainer bits and the lower nibble
        of the mapper number.

    flags_7: int
        Raw header byte 7. It stores console/file-format bits and the upper
        nibble of the mapper number.

Why keep raw flags too?
Even if we do not use every bit today, keeping flags_6 and flags_7 preserves the
parsed facts so future mapper/mirroring features can use them without reparsing
the original file bytes.
"""

import dataclasses
import importlib


def test_ines_header_class_exists_and_is_frozen_dataclass():
    """
    Objective:
    Create INesHeader as a frozen dataclass.

    Why frozen:
    Parsed header data is a fact about the file. It should not change during
    emulation.
    """
    ines = importlib.import_module("emulator.cartridge.ines")

    assert hasattr(ines, "INesHeader")
    assert dataclasses.is_dataclass(ines.INesHeader)
    assert ines.INesHeader.__dataclass_params__.frozen is True


def test_ines_header_has_required_fields_in_order():
    """
    Objective:
    Store all header fields needed by the next parser steps.
    """
    ines = importlib.import_module("emulator.cartridge.ines")

    assert list(ines.INesHeader.__dataclass_fields__) == [
        "prg_rom_banks",
        "chr_rom_banks",
        "mapper_number",
        "has_trainer",
        "flags_6",
        "flags_7",
    ]


def test_ines_header_can_store_parsed_values():
    """
    Objective:
    INesHeader should be a small container for parsed header values.
    """
    ines = importlib.import_module("emulator.cartridge.ines")

    header = ines.INesHeader(
        prg_rom_banks=1,
        chr_rom_banks=1,
        mapper_number=0,
        has_trainer=False,
        flags_6=0x00,
        flags_7=0x00,
    )

    assert header.prg_rom_banks == 1
    assert header.chr_rom_banks == 1
    assert header.mapper_number == 0
    assert header.has_trainer is False
    assert header.flags_6 == 0x00
    assert header.flags_7 == 0x00
