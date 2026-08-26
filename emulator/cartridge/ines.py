from dataclasses import dataclass

INES_MAGIC = b"NES\x1A"
INES_HEADER_SIZE = 16
TRAINER_SIZE = 512
PRG_ROM_BANK_SIZE = 16 * 1024
CHR_ROM_BANK_SIZE = 8 * 1024
FLAGS6_VERTICAL_MIRRORING = 1 << 0

@dataclass(frozen=True) # not mutable data
class INesHeader: 
    prg_rom_banks: int
    chr_rom_banks: int 
    mapper_number: int
    has_trainer: bool # Extra 512 bytes "trainer" present?
    flags_6: int # Has lower nybble of mapper number
    flags_7: int # Has upper nybble of mapper number
    
    @property
    def is_vertical_mirroring(self) -> bool:
        return (self.flags_6 & FLAGS6_VERTICAL_MIRRORING) != 0
    

def parse_ines_header(data: bytes) -> INesHeader:
    # 1 Verify len data bigger than header size
    if len(data) < INES_HEADER_SIZE:
        raise ValueError("iNES data is too short")

    # 2. Verify Magic bytes are OK
    if data[0:4] != INES_MAGIC:
        raise ValueError("Invalid iNES header")

    # 3. Parse fields
    prg_rom_banks = data[4] # Byte 4 stores the number of 16KB PRG ROM banks.
    chr_rom_banks = data[5] # Byte 5 stores the number of 8KB CHR ROM banks.
    flags_6 = data[6] 
    flags_7 = data[7]
    has_trainer = (flags_6 & 0b0000_0100) != 0
    mapper_number = (flags_6 >> 4) | (flags_7 & 0xF0)

    # 4. Return new INesHeader
    return INesHeader(prg_rom_banks, chr_rom_banks, mapper_number, has_trainer, flags_6, flags_7)



@dataclass(frozen=True) # Not mutable data
class INesRom:
    header: INesHeader
    prg_rom: bytes
    chr_rom: bytes

def parse_ines_rom(data: bytes) -> INesRom:
    # 1. Parse iNES Header
    header = parse_ines_header(data)
    # 2. Determine program size 
    prg_size = header.prg_rom_banks * PRG_ROM_BANK_SIZE
    chr_size = header.chr_rom_banks * CHR_ROM_BANK_SIZE 
    # 3. Where program data starts? and where it ends?
    prg_start = INES_HEADER_SIZE + (TRAINER_SIZE if header.has_trainer else 0) # byte after header + trainer if present
    prg_end = prg_start + prg_size
    # 4. Where character data starts? and where it ends?
    chr_start = prg_end
    chr_end = chr_start + chr_size

    # 5. Validation: character data end position is less than original data length
    if len(data) < chr_end:
        raise ValueError("iNES data is too short for declared PRG/CHR ROM")
    
    # 6. Return new INesRom
    return INesRom(header=header, 
                   prg_rom=data[prg_start:prg_end], 
                   chr_rom=data[chr_start:chr_end])


    

    
    
