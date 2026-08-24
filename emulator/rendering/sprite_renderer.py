from emulator.ppu.chr_decoder import decode_chr_tile
from emulator.rendering.framebuffer import Framebuffer
from emulator.rendering.nametable_renderer import BackgroundOpaqueMask
from emulator.rendering.palette_ram import SpritePalettes

from dataclasses import dataclass

OAM_SPRITE_COUNT = 64
BYTES_PER_SPRITE = 4
OAM_SIZE = OAM_SPRITE_COUNT * BYTES_PER_SPRITE

SPRITE_PALETTE_ID_MASK = 0b0000_0011
SPRITE_IS_BEHIND_BACKGROUND = 1 << 5
SPRITE_FLIP_HORIZONTAL = 1 << 6
SPRITE_FLIP_VERTICAL = 1 << 7

@dataclass(frozen=True)
class SpriteEntry:
    y: int
    tile_index: int
    attributes: int
    x: int

@dataclass(frozen=True)
class SpriteAttributes:
    palette_id: int
    is_behind_background: bool
    flip_horizontal: bool
    flip_vertical: bool

def decode_sprite_entry(oam: bytes | bytearray, sprite_index: int) -> SpriteEntry:
    if len(oam) < OAM_SIZE:
        raise ValueError("OAM must contain 256 bytes")

    if not 0 <= sprite_index < OAM_SPRITE_COUNT:
        raise ValueError("sprite_index must be in range 0..63")

    base = sprite_index * BYTES_PER_SPRITE

    return SpriteEntry(
        y=oam[base],
        tile_index=oam[base + 1],
        attributes=oam[base + 2],
        x=oam[base + 3],
    )

def decode_sprite_attributes(attributes: int) -> SpriteAttributes:
    attributes &= 0xFF # Ensure size is 1 byte

    return SpriteAttributes(
        palette_id=attributes & SPRITE_PALETTE_ID_MASK,
        is_behind_background=(attributes & SPRITE_IS_BEHIND_BACKGROUND) != 0,
        flip_horizontal=(attributes & SPRITE_FLIP_HORIZONTAL) != 0,
        flip_vertical=(attributes & SPRITE_FLIP_VERTICAL) != 0,
    )

def render_sprite_8x8_to_framebuffer(
        framebuffer: Framebuffer,
        sprite: SpriteEntry,
        pattern_table: bytes,
        sprite_palettes: SpritePalettes,
        background_opaque_mask: BackgroundOpaqueMask | None = None,
) -> None:

    attributes = decode_sprite_attributes(sprite.attributes)

    tile_start = sprite.tile_index * 16
    tile_end = tile_start + 16

    if tile_end > len(pattern_table):
        raise ValueError("Pattern table does not contain sprite tile bytes")

    tile_bytes = pattern_table[tile_start:tile_end]
    color_indexes = decode_chr_tile(tile_bytes)
    palette = sprite_palettes[attributes.palette_id]

    for tile_y in range(8):
        for tile_x in range(8):
            source_x = 7 - tile_x if attributes.flip_horizontal else tile_x
            source_y = 7 - tile_y if attributes.flip_vertical else tile_y

            color_index = color_indexes[source_y][source_x]

            if color_index == 0: # Set as transparent
                continue

            screen_x = sprite.x + tile_x
            screen_y = sprite.y + tile_y

            if not (0 <= screen_x < framebuffer.width):
                continue
            if not (0 <= screen_y < framebuffer.height):
                continue

            if (background_opaque_mask is not None
                and attributes.is_behind_background
                and background_opaque_mask[screen_y * framebuffer.width + screen_x]
            ): 
                continue
            
            framebuffer.set_pixel(
                screen_x,
                screen_y,
                palette[color_index],
            )

def render_oam_sprites_to_framebuffer(
    framebuffer: Framebuffer,
    oam: bytes | bytearray,
    pattern_table: bytes,
    sprite_palettes: SpritePalettes,
    background_opaque_mask: BackgroundOpaqueMask | None = None,
) -> None:
    if len(oam) < OAM_SIZE:
        raise ValueError("OAM must contain 256 bytes")

    # First sprite is the last rendered, to appear upfront
    for sprite_index in reversed(range(OAM_SPRITE_COUNT)):
        sprite = decode_sprite_entry(oam, sprite_index)
        render_sprite_8x8_to_framebuffer(
            framebuffer,
            sprite,
            pattern_table,
            sprite_palettes,
            background_opaque_mask,
        )
