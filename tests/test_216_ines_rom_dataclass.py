"""
Create the INesRom data class.

Class to implement:
    INesRom

Why this class exists:
Once the header is parsed, the emulator needs one object that keeps the parsed
metadata together with the actual ROM sections:

    header: INesHeader
        The parsed iNES header. It tells us how many PRG/CHR banks exist,
        whether a trainer was present, and which mapper number the cartridge
        declares.

    PRG ROM
        Program bytes used by the CPU.

    CHR ROM
        Graphics pattern bytes used by the PPU later.

INesRom groups:
    - header: INesHeader
    - prg_rom: bytes
    - chr_rom: bytes

This keeps parse_ines_rom(data) clean: it can return one object containing both
metadata and extracted sections.
"""

import dataclasses
import importlib


def test_ines_rom_class_exists_and_is_frozen_dataclass():
    """
    Objective:
    Create INesRom as a frozen dataclass.

    Why frozen:
    Parsed ROM sections are facts extracted from the file. They should not be
    mutated by the parser result object.
    """
    ines = importlib.import_module("emulator.cartridge.ines")

    assert hasattr(ines, "INesRom")
    assert dataclasses.is_dataclass(ines.INesRom)
    assert ines.INesRom.__dataclass_params__.frozen is True


def test_ines_rom_has_required_fields_in_order():
    """Objective: INesRom stores header, PRG ROM, and CHR ROM."""
    ines = importlib.import_module("emulator.cartridge.ines")

    assert list(ines.INesRom.__dataclass_fields__) == [
        "header",
        "prg_rom",
        "chr_rom",
    ]


def test_ines_rom_can_store_header_prg_and_chr_bytes():
    """
    Objective:
    INesRom should group parsed metadata with extracted ROM byte sections.
    """
    ines = importlib.import_module("emulator.cartridge.ines")
    header = ines.INesHeader(1, 1, 0, False, 0x00, 0x00)

    rom = ines.INesRom(
        header=header,
        prg_rom=bytes([0xA9, 0x42]),
        chr_rom=bytes([0x00, 0x01]),
    )

    assert rom.header is header
    assert rom.prg_rom == bytes([0xA9, 0x42])
    assert rom.chr_rom == bytes([0x00, 0x01])
