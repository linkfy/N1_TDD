"""
Implement parse_ines_rom(data).

Function to implement:
    parse_ines_rom(data: bytes) -> INesRom

Why this function exists:
parse_ines_header(data) tells us what the file claims to contain. parse_ines_rom
uses those header facts to extract the actual PRG ROM and CHR ROM byte sections.

Implementation guide:

1. Parse the iNES header.

       header = parse_ines_header(data)

2. Compute declared section sizes.

       prg_size = header.prg_rom_banks * PRG_ROM_BANK_SIZE
       chr_size = header.chr_rom_banks * CHR_ROM_BANK_SIZE

3. Compute where PRG ROM starts.

       prg_start = INES_HEADER_SIZE + (TRAINER_SIZE if header.has_trainer else 0)

   Why:
   PRG ROM starts after the 16-byte header. If a trainer exists, skip those 512
   bytes too.

4. Compute section boundaries.

       prg_end = prg_start + prg_size
       chr_start = prg_end
       chr_end = chr_start + chr_size

5. Validate the input contains all declared bytes.

       if len(data) < chr_end:
           raise ValueError("iNES data is too short for declared PRG/CHR ROM")

6. Return INesRom with slices.

       return INesRom(
           header=header,
           prg_rom=data[prg_start:prg_end],
           chr_rom=data[chr_start:chr_end],
       )

Why this step matters before Cartridge/Mapper work:
The mapper should receive clean PRG ROM bytes. It should not need to understand
iNES headers or trainer offsets. This parser isolates that file-format work.
"""

import importlib

import pytest


def make_ines_data(
    prg_banks=1,
    chr_banks=1,
    flags_6=0x00,
    flags_7=0x00,
    trainer=None,
    prg_byte=0xAA,
    chr_byte=0xBB,
):
    ines = importlib.import_module("emulator.cartridge.ines")

    header = bytearray(16)
    header[0:4] = b"NES\x1A"
    header[4] = prg_banks
    header[5] = chr_banks
    header[6] = flags_6
    header[7] = flags_7

    prg = bytes([prg_byte]) * (prg_banks * ines.PRG_ROM_BANK_SIZE)
    chr_ = bytes([chr_byte]) * (chr_banks * ines.CHR_ROM_BANK_SIZE)

    if trainer is None:
        trainer = b""

    return bytes(header) + trainer + prg + chr_


def test_parse_ines_rom_function_exists():
    """Objective: expose parse_ines_rom(data)."""
    ines = importlib.import_module("emulator.cartridge.ines")

    assert hasattr(ines, "parse_ines_rom")
    assert callable(ines.parse_ines_rom)


def test_parse_ines_rom_extracts_prg_and_chr_sections():
    """
    Objective:
    Extract PRG ROM and CHR ROM according to header bank counts.
    """
    ines = importlib.import_module("emulator.cartridge.ines")
    data = make_ines_data(prg_banks=1, chr_banks=1, prg_byte=0xAA, chr_byte=0xBB)

    rom = ines.parse_ines_rom(data)

    assert rom.header.prg_rom_banks == 1
    assert rom.header.chr_rom_banks == 1
    assert len(rom.prg_rom) == ines.PRG_ROM_BANK_SIZE
    assert len(rom.chr_rom) == ines.CHR_ROM_BANK_SIZE
    assert rom.prg_rom == bytes([0xAA]) * ines.PRG_ROM_BANK_SIZE
    assert rom.chr_rom == bytes([0xBB]) * ines.CHR_ROM_BANK_SIZE


def test_parse_ines_rom_supports_multiple_prg_banks():
    """
    Objective:
    Header byte 4 is a PRG bank count. Two banks means 32KB of PRG ROM.
    """
    ines = importlib.import_module("emulator.cartridge.ines")
    data = make_ines_data(prg_banks=2, chr_banks=1)

    rom = ines.parse_ines_rom(data)

    assert len(rom.prg_rom) == 2 * ines.PRG_ROM_BANK_SIZE


def test_parse_ines_rom_skips_trainer_when_present():
    """
    Objective:
    If flags_6 bit 2 is set, skip the 512-byte trainer before PRG ROM.
    """
    ines = importlib.import_module("emulator.cartridge.ines")
    trainer = bytes([0xCC]) * ines.TRAINER_SIZE
    data = make_ines_data(
        flags_6=0b0000_0100,
        trainer=trainer,
        prg_byte=0xAA,
        chr_byte=0xBB,
    )

    rom = ines.parse_ines_rom(data)

    assert rom.header.has_trainer is True
    assert rom.prg_rom[0] == 0xAA
    assert rom.chr_rom[0] == 0xBB
    assert 0xCC not in rom.prg_rom[:16]


def test_parse_ines_rom_rejects_data_shorter_than_declared_sections():
    """
    Objective:
    If the header declares PRG/CHR bytes that are missing, reject the file.
    """
    ines = importlib.import_module("emulator.cartridge.ines")
    data = make_ines_data(prg_banks=1, chr_banks=1)
    truncated = data[:-1]

    with pytest.raises(ValueError, match="iNES data is too short for declared PRG/CHR ROM"):
        ines.parse_ines_rom(truncated)


def test_parse_ines_rom_returns_header_and_sections_together():
    """
    Objective:
    parse_ines_rom should return INesRom(header, prg_rom, chr_rom), not loose
    values.
    """
    ines = importlib.import_module("emulator.cartridge.ines")
    data = make_ines_data(prg_banks=1, chr_banks=1, flags_6=0x20, flags_7=0x40)

    rom = ines.parse_ines_rom(data)

    assert isinstance(rom, ines.INesRom)
    assert isinstance(rom.header, ines.INesHeader)
    assert rom.header.mapper_number == 0x42
