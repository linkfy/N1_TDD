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
        tile_index=oam[base+1],
        attributes=oam[base+2],
        x=oam[base+3],
    )



def decode_sprite_attributes(attributes: int) -> SpriteAttributes:
    attributes &= 0xFF # Ensure size is 1 byte

    return SpriteAttributes(
        palette_id=attributes & SPRITE_PALETTE_ID_MASK,
        is_behind_background=(attributes & SPRITE_IS_BEHIND_BACKGROUND) != 0,
        flip_horizontal=(attributes & SPRITE_FLIP_HORIZONTAL) != 0,
        flip_vertical=(attributes & SPRITE_FLIP_VERTICAL) != 0,
    )
