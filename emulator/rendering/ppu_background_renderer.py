"""
Read nametable bytes     $2000-$23BF
Read attribute bytes    $23C0-$23FF
Read palette RAM        $3F00-$3F0F
Read pattern table bytes for selected one by PPUCTRL $0000 or $1000
Output framebuffer
"""


from emulator.ppu.ppu import PPU, CTRL_BACKGROUND_PATTERN_TABLE
from emulator.rendering.framebuffer import Framebuffer
from emulator.rendering.nametable_renderer import (
    BackgroundOpaqueMask, 
    build_background_opaque_mask, 
    nametable_with_palette_ram_to_framebuffer, 
    NAMETABLE_SIZE
)
from emulator.rendering.palette_ram import PALETTE_RAM_SIZE
from emulator.ppu.chr_decoder import PATTERN_TABLE_SIZE

BASE_NAMETABLE_ADDR = 0x2000
BASE_ATTR_TABLE_ADDR = 0x23C0
PALETTE_RAM_ADDR = 0x3F00

PATTERN_TABLE_0_ADDR = 0x0000
PATTERN_TABLE_1_ADDR = 0x1000
ATTR_TABLE_SIZE = 64


def ppu_background_to_framebuffer(ppu: PPU) -> Framebuffer:
    
    nametable_bytes = bytes(
            ppu.ppu_bus.read(BASE_NAMETABLE_ADDR + offset)
        for offset in range(NAMETABLE_SIZE)
    )
    
    attribute_table = bytes(
        ppu.ppu_bus.read(BASE_ATTR_TABLE_ADDR + offset)
        for offset in range(ATTR_TABLE_SIZE)
    )

    pattern_table_base = (
        PATTERN_TABLE_1_ADDR 
        if ppu.ctrl & CTRL_BACKGROUND_PATTERN_TABLE
        else PATTERN_TABLE_0_ADDR
    )

    pattern_table_bytes = bytes(
        ppu.ppu_bus.read(pattern_table_base + offset)
        for offset in range(PATTERN_TABLE_SIZE)
    )

    palette_ram = bytes(
        ppu.ppu_bus.read(PALETTE_RAM_ADDR + offset)
        for offset in range(PALETTE_RAM_SIZE)
    )

    return nametable_with_palette_ram_to_framebuffer(
        nametable_bytes,
        attribute_table,
        pattern_table_bytes,
        palette_ram,
    )
    
def ppu_background_to_opaque_mask(ppu: PPU) -> BackgroundOpaqueMask:

    nametable_bytes = bytes(
        ppu.ppu_bus.read(BASE_NAMETABLE_ADDR + offset)
        for offset in range(NAMETABLE_SIZE)
    )
    
    pattern_table_base = (
        PATTERN_TABLE_1_ADDR 
        if ppu.ctrl & CTRL_BACKGROUND_PATTERN_TABLE
        else PATTERN_TABLE_0_ADDR
    )

    pattern_table_bytes = bytes(
        ppu.ppu_bus.read(pattern_table_base + offset)
        for offset in range(PATTERN_TABLE_SIZE)
    )

    return build_background_opaque_mask(
        pattern_table=pattern_table_bytes,
        nametable=nametable_bytes,
    ) 
