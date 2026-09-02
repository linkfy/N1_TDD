SpriteZeroHitPosition = tuple[int, int]

from emulator.ppu.chr_decoder import PATTERN_TABLE_SIZE, decode_chr_tile
from emulator.ppu.ppu import CTRL_SPRITE_PATTERN_TABLE, PPU
from emulator.rendering.nametable_renderer import BackgroundOpaqueMask
from emulator.rendering.framebuffer import NES_SCREEN_HEIGHT, NES_SCREEN_WIDTH
from emulator.rendering.sprite_renderer import (
        SpriteEntry, 
        decode_sprite_attributes, 
        decode_sprite_entry
)
from emulator.rendering.ppu_background_renderer import (
        PATTERN_TABLE_0_ADDR,
        PATTERN_TABLE_1_ADDR,
        ppu_background_viewport_to_opaque_mask as ppu_background_to_opaque_mask
)


def find_sprite_zero_hit_position(
        sprite_zero: SpriteEntry,
        pattern_table: bytes,
        background_opaque_mask: BackgroundOpaqueMask,
        screen_width: int = NES_SCREEN_WIDTH,
        screen_height: int = NES_SCREEN_HEIGHT,
) -> SpriteZeroHitPosition | None:
    if len(background_opaque_mask) != screen_width * screen_height:
        raise ValueError("Background opaque mask size must be equal to screen width * height")
    
    tile_start = sprite_zero.tile_index * 16
    tile_end = tile_start + 16

    if tile_end > len(pattern_table):
        raise ValueError("Pattern table does not contain sprite 0 tile bytes")

    # Decode Sprite 0 Tile and attributes
    attributes = decode_sprite_attributes(sprite_zero.attributes)
    color_indexes = decode_chr_tile(pattern_table[tile_start:tile_end])

    # Find first opaque pixel overlap
    for tile_y in range(8):
        for tile_x in range(8):
            source_x = 7 - tile_x if attributes.flip_horizontal else tile_x
            source_y = 7 - tile_y if attributes.flip_vertical else tile_y

            sprite_color_index = color_indexes[source_y][source_x]
            
            if sprite_color_index == 0:
                continue

            screen_x = sprite_zero.x + tile_x
            screen_y = sprite_zero.y + tile_y

            if not (0 <= screen_x < screen_width):
                continue
            if not (0 <= screen_y < screen_height):
                continue

            mask_index = screen_y * screen_width + screen_x
            # HIT!
            if background_opaque_mask[mask_index]:
                return screen_x, screen_y

    return None
            
def ppu_sprite_zero_hit_position(ppu: PPU) -> SpriteZeroHitPosition | None:
    sprite_zero = decode_sprite_entry(oam=ppu.oam, sprite_index=0)

    background_opaque_mask = ppu_background_to_opaque_mask(ppu)

    sprite_pattern_table_base = (
        PATTERN_TABLE_1_ADDR
        if ppu.ctrl & CTRL_SPRITE_PATTERN_TABLE
        else PATTERN_TABLE_0_ADDR
    )

    sprite_pattern_table = bytes(
        ppu.ppu_bus.read(sprite_pattern_table_base + offset)
        for offset in range(PATTERN_TABLE_SIZE)
    )

    return find_sprite_zero_hit_position(
        sprite_zero=sprite_zero,
        pattern_table=sprite_pattern_table,
        background_opaque_mask=background_opaque_mask,
    )
