from emulator.cartridge.cartridge import Cartridge
from emulator.cartridge.mapper000 import Mapper000


def create_mapper(cartridge: Cartridge):
    if cartridge.mapper_number == 0:
        return Mapper000(
            prg_rom=cartridge.prg_rom,
            chr_rom=cartridge.chr_rom,
            is_vertical_mirroring=cartridge.is_vertical_mirroring,
        )

    raise ValueError(f"Unsupported mapper: {cartridge.mapper_number}")
