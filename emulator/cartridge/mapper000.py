from dataclasses import dataclass

PRG_ROM_START = 0x8000
PRG_ROM_END = 0xFFFF
NROM_128_SIZE = 16 * 1024
NROM_256_SIZE = 32 * 1024

CHR_ROM_START = 0x0000
CHR_ROM_END = 0x1FFF
CHR_ROM_SIZE = 8 * 1024

@dataclass
class Mapper000:
    prg_rom: bytes
    chr_rom: bytes

    def read_prg(self, addr: int) -> int:
        # 1. Verify addr is in Mapper000 ROM area range
        if not (PRG_ROM_START <= addr <= PRG_ROM_END):
            raise ValueError(f"Address out of PRG ROM range: {addr:04X}")

        # 2. Transform received to ROM address
        if len(self.prg_rom) == NROM_128_SIZE: # 16 KB Case
            # If ROM is 16KB we mirror the values to the next 16KB addresses
            offset = (addr - PRG_ROM_START) % NROM_128_SIZE
        elif len(self.prg_rom) == NROM_256_SIZE: # 32 KB Case
            offset = addr - PRG_ROM_START
        else:
            raise ValueError("Mapper000 supports only 16KB or 32KB PRG ROM")
        
        return self.prg_rom[offset]

    def read_chr(self, addr: int) -> int:
        # 1. Verify addr is in Mapper000 CHR-ROM area range
        if not (CHR_ROM_START <= addr <= CHR_ROM_END):
            raise ValueError(f"Address out of CHR ROM range: {addr:04X}")
        if len(self.chr_rom) != CHR_ROM_SIZE:
            raise ValueError("Mapper000 expects 8KB CHR ROM")

        # 2. Transform received to CHR-ROM address
        offset = addr - CHR_ROM_START
        
        return self.chr_rom[offset]

    def write_chr(self, addr: int, value: int) -> None:
        if not (CHR_ROM_START <= addr <= CHR_ROM_END):
            raise ValueError(f"Address out of CHR ROM range: {addr:04X}")
        raise ValueError("CHR ROM is read-only for official Mapper000")
