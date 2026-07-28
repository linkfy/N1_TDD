"""
Create the Cartridge object from parsed iNES data.

File to create:
    emulator/cartridge/cartridge.py

Class to implement:
    Cartridge

Why this step exists:
The iNES parser understands the .nes file format:

    raw .nes bytes -> INesRom(header, prg_rom, chr_rom)

But the rest of the emulator should not need to work directly with iNES parser
objects. It should work with a cartridge-level object:

    Cartridge(prg_rom, chr_rom, mapper_number, chr_ram=None)

Responsibilities of Cartridge at this stage:
    - store PRG ROM bytes
    - store CHR ROM bytes
    - store mapper number declared by the ROM
    - optionally expose CHR RAM storage for cartridges that need it later
    - provide from_ines_bytes(data) as a convenient constructor

Why chr_ram exists now:
Some cartridges do not contain CHR ROM. In iNES, this usually appears as zero
CHR ROM banks. Those cartridges use writable CHR RAM instead, so games can upload
tile graphics at runtime.

We add chr_ram to the Cartridge shape now to keep the future mapper/PPU-bus path
stable. It is allowed to be None by default because Mapper000 CHR RAM behavior is
not implemented in this step yet.

Future use:
    - PpuBus will route PPU $0000-$1FFF to the mapper
    - mappers may read from CHR ROM or writable CHR RAM
    - more advanced mappers may use different CHR banking behavior

What Cartridge should NOT do yet:
    - translate CPU addresses
    - mirror PRG ROM
    - implement mapper behavior
    - know about CPU bus reads

Those responsibilities belong to mapper classes and CpuBus integration later.

Expected implementation shape:

    from dataclasses import dataclass
    from emulator.cartridge.ines import parse_ines_rom


    @dataclass
    class Cartridge:
        prg_rom: bytes
        chr_rom: bytes
        mapper_number: int
        chr_ram: bytearray | None = None

        @classmethod
        def from_ines_bytes(cls, data: bytes) -> "Cartridge":
            ines_rom = parse_ines_rom(data)
            return cls(
                prg_rom=ines_rom.prg_rom,
                chr_rom=ines_rom.chr_rom,
                mapper_number=ines_rom.header.mapper_number,
                chr_ram=None,
            )
"""

import dataclasses
import inspect
from pathlib import Path

from emulator.cartridge.cartridge import Cartridge
from emulator.cartridge.ines import CHR_ROM_BANK_SIZE, PRG_ROM_BANK_SIZE


def make_ines_data(
    prg_banks=1,
    chr_banks=1,
    flags_6=0x00,
    flags_7=0x00,
    prg_byte=0xAA,
    chr_byte=0xBB,
):
    header = bytearray(16)
    header[0:4] = b"NES\x1A"
    header[4] = prg_banks
    header[5] = chr_banks
    header[6] = flags_6
    header[7] = flags_7

    prg_rom = bytes([prg_byte]) * (prg_banks * PRG_ROM_BANK_SIZE)
    chr_rom = bytes([chr_byte]) * (chr_banks * CHR_ROM_BANK_SIZE)

    return bytes(header) + prg_rom + chr_rom


def test_cartridge_file_exists():
    """
    Objective:
    Create emulator/cartridge/cartridge.py.

    Why separate from ines.py:
    ines.py parses a file format. cartridge.py represents the cartridge data that
    the rest of the emulator will use.
    """
    assert Path("emulator/cartridge/cartridge.py").exists()


def test_cartridge_is_dataclass():
    """
    Objective:
    Cartridge should be a dataclass.

    Why not frozen anymore:
    Cartridge can optionally expose CHR RAM. CHR RAM is writable graphics memory
    for cartridges that do not provide CHR ROM. Keeping Cartridge non-frozen
    avoids mixing a frozen container with intentionally mutable CHR RAM state.
    """
    assert dataclasses.is_dataclass(Cartridge)


def test_cartridge_has_required_fields_in_order():
    """
    Objective:
    Cartridge stores the emulator-facing cartridge data.
    """
    assert list(Cartridge.__dataclass_fields__) == [
        "prg_rom",
        "chr_rom",
        "mapper_number",
        "chr_ram",
    ]


def test_cartridge_can_be_created_directly():
    """
    Objective:
    Cartridge is a simple data object and can be constructed with explicit data.
    """
    cartridge = Cartridge(
        prg_rom=bytes([0xA9, 0x42]),
        chr_rom=bytes([0x00, 0x01]),
        mapper_number=0,
    )

    assert cartridge.prg_rom == bytes([0xA9, 0x42])
    assert cartridge.chr_rom == bytes([0x00, 0x01])
    assert cartridge.mapper_number == 0
    assert cartridge.chr_ram is None


def test_cartridge_can_optionally_store_chr_ram():
    """
    Objective:
    Cartridge can optionally expose CHR RAM for future mapper/PPU-bus behavior.

    Why optional:
    Cartridges with CHR ROM do not need writable CHR RAM. Cartridges with no CHR
    ROM banks may use CHR RAM instead, but that behavior will be wired through
    mappers and PpuBus in later steps.
    """
    chr_ram = bytearray(8 * 1024)
    cartridge = Cartridge(
        prg_rom=bytes([0x00]),
        chr_rom=b"",
        mapper_number=0,
        chr_ram=chr_ram,
    )

    assert cartridge.chr_ram is chr_ram


def test_cartridge_has_from_ines_bytes_classmethod():
    """
    Objective:
    Provide Cartridge.from_ines_bytes(data).

    Why:
    The caller can pass raw .nes bytes and receive a Cartridge without manually
    calling parse_ines_rom.
    """
    assert hasattr(Cartridge, "from_ines_bytes")
    assert callable(Cartridge.from_ines_bytes)
    assert list(inspect.signature(Cartridge.from_ines_bytes).parameters) == ["data"]


def test_from_ines_bytes_extracts_prg_and_chr_rom():
    """
    Objective:
    from_ines_bytes should use the iNES parser and store extracted PRG/CHR ROM.
    """
    data = make_ines_data(prg_banks=1, chr_banks=1, prg_byte=0xAA, chr_byte=0xBB)

    cartridge = Cartridge.from_ines_bytes(data)

    assert cartridge.prg_rom == bytes([0xAA]) * PRG_ROM_BANK_SIZE
    assert cartridge.chr_rom == bytes([0xBB]) * CHR_ROM_BANK_SIZE


def test_from_ines_bytes_copies_mapper_number_from_header():
    """
    Objective:
    Cartridge should expose the mapper number declared by the iNES header.

    Example:
        flags_6 = 0x20 contributes mapper low nibble 0x02
        flags_7 = 0x40 contributes mapper upper nibble 0x40
        mapper_number = 0x42
    """
    data = make_ines_data(flags_6=0x20, flags_7=0x40)

    cartridge = Cartridge.from_ines_bytes(data)

    assert cartridge.mapper_number == 0x42


def test_cartridge_does_not_implement_mapper_address_translation_yet():
    """
    Objective:
    Keep Cartridge small at this stage.

    Address translation belongs to mapper classes, not this data object.
    """
    assert not hasattr(Cartridge, "read_prg")
    assert not hasattr(Cartridge, "cpu_read")
