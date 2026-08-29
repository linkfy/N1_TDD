"""
Example with first nametable
Read nametable bytes    $2000-$23BF <= First nametable example of 4: ($2000, $2400, $2800, $2C00)
Read attribute bytes    $23C0-$23FF <= First nametable example 
-----------------------------------
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
from emulator.rendering.background_viewport import (
    compose_horizontal_framebuffer_viewport,
    compose_horizontal_opaque_mask_viewport,
    decode_background_viewport_position,
)

BASE_NAMETABLE_ADDR = 0x2000
BASE_ATTR_TABLE_ADDR = 0x23C0
PALETTE_RAM_ADDR = 0x3F00

PATTERN_TABLE_0_ADDR = 0x0000
PATTERN_TABLE_1_ADDR = 0x1000
ATTR_TABLE_SIZE = 64

LOGICAL_NAMETABLE_BASE_ADDRS = (
    0x2000,
    0x2400,
    0x2800,
    0x2C00,
)


def ppu_background_to_framebuffer(
        ppu: PPU, 
        base_nametable_addr: int = BASE_NAMETABLE_ADDR
) -> Framebuffer:

    if base_nametable_addr not in LOGICAL_NAMETABLE_BASE_ADDRS:
        raise ValueError(
            "Logical nametable base address must be $2000, $2400, $2800, $2C00"
        )
    
    nametable_bytes = bytes(
            ppu.ppu_bus.read(base_nametable_addr + offset)
        for offset in range(NAMETABLE_SIZE)
    )
    
    attribute_table_base = base_nametable_addr + NAMETABLE_SIZE
    attribute_table = bytes(
        ppu.ppu_bus.read(attribute_table_base + offset)
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
    
def ppu_background_to_opaque_mask(
        ppu: PPU,
        base_nametable_addr: int = BASE_NAMETABLE_ADDR,
) -> BackgroundOpaqueMask:

    if base_nametable_addr not in LOGICAL_NAMETABLE_BASE_ADDRS:
        raise ValueError(
            "Logical nametable base address must be $2000, $2400, $2800, $2C00"
        )
    
    nametable_bytes = bytes(
        ppu.ppu_bus.read(base_nametable_addr + offset)
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

def ppu_background_viewport_to_framebuffer(ppu: PPU) -> Framebuffer:
    viewport_x, _ = decode_background_viewport_position(
        temp_vram_addr=ppu.temp_vram_addr,
        fine_x=ppu.fine_x
    )

    nametable_y = (ppu.temp_vram_addr >> 11)  & 1

    # Each horizontal pair is $800-byte ($400 x 2)
    left_base = BASE_NAMETABLE_ADDR + nametable_y * 0x800
    right_base = left_base + 0x400

    left = ppu_background_to_framebuffer(
        ppu,
        base_nametable_addr=left_base,
    )
    right = ppu_background_to_framebuffer(
        ppu,
        base_nametable_addr=right_base,
    )

    return compose_horizontal_framebuffer_viewport(
        left=left,
        right=right,
        viewport_x=viewport_x,
    )


def ppu_background_viewport_to_opaque_mask(ppu: PPU) -> BackgroundOpaqueMask:
    # Use same logic as ppu_background_viewport_to_framebuffer with correct functions
    viewport_x, _ = decode_background_viewport_position(
        temp_vram_addr=ppu.temp_vram_addr,
        fine_x=ppu.fine_x
    )

    nametable_y = (ppu.temp_vram_addr >> 11)  & 1

    # Each horizontal pair is $800-byte ($400 x 2)
    left_base = BASE_NAMETABLE_ADDR + nametable_y * 0x800
    right_base = left_base + 0x400

    left = ppu_background_to_opaque_mask(
        ppu,
        base_nametable_addr=left_base,
    )
    right = ppu_background_to_opaque_mask(
        ppu,
        base_nametable_addr=right_base,
    )

    return compose_horizontal_opaque_mask_viewport(
        left=left,
        right=right,
        viewport_x=viewport_x,
    )


