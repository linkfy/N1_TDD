"""
Create the iNES parser file and top-level constants.

File to create:
    emulator/cartridge/ines.py

Why a new cartridge folder?
The iNES format describes a NES cartridge file. It is not just generic memory.

    emulator/memory/rom.py
        Generic read-only bytes.

    emulator/cartridge/ines.py
        Knows how to parse the .nes/iNES file format.

Design rule:
Keep file-format parsing separate from CPU execution, CPU bus mapping, and raw
memory devices.

Constants to define:
    INES_MAGIC = b"NES\x1A"
        The first four bytes that identify an iNES file.

    INES_HEADER_SIZE = 16
        Every iNES file starts with a 16-byte header.

    TRAINER_SIZE = 512
        Some old ROMs include an optional 512-byte trainer after the header.

    PRG_ROM_BANK_SIZE = 16 * 1024
        Header byte 4 stores the number of 16KB PRG ROM banks.
        PRG ROM is program code/data visible to the CPU.

    CHR_ROM_BANK_SIZE = 8 * 1024
        Header byte 5 stores the number of 8KB CHR ROM banks.
        CHR ROM is graphics pattern data used by the PPU later.

Why this is the first iNES step:
Before parsing fields or extracting ROM sections, students need stable names for
the file-format sizes. This keeps later code readable and avoids magic numbers
like 16, 512, 16384, and 8192 spread through the parser.
"""

import importlib
from pathlib import Path


def test_cartridge_folder_and_ines_file_exist():
    """
    Objective:
    Create a new cartridge folder and an ines.py file inside it.
    """
    assert Path("emulator/cartridge").exists()
    assert Path("emulator/cartridge/ines.py").exists()


def test_ines_module_defines_file_format_constants():
    """
    Objective:
    Define the top-level iNES constants used by the parser.

    These constants describe the binary layout of a .nes file.
    """
    ines = importlib.import_module("emulator.cartridge.ines")

    assert ines.INES_MAGIC == b"NES\x1A"
    assert ines.INES_HEADER_SIZE == 16
    assert ines.TRAINER_SIZE == 512
    assert ines.PRG_ROM_BANK_SIZE == 16 * 1024
    assert ines.CHR_ROM_BANK_SIZE == 8 * 1024
