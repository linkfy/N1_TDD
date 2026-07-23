from dataclasses import dataclass
from emulator.cartridge.ines import parse_ines_rom


@dataclass(frozen=True)
class Cartridge:
    prg_rom: bytes
    chr_rom: bytes
    mapper_number: int
    
    @classmethod
    def from_ines_bytes(cls, data: bytes) -> "Cartridge":
        ines_rom = parse_ines_rom(data)
        return cls(
            prg_rom=ines_rom.prg_rom,
            chr_rom=ines_rom.chr_rom,
            mapper_number=ines_rom.header.mapper_number
        )
