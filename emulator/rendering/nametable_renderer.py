"""
A nametable is PPU memory that says which tile appears at each background cell
https://www.nesdev.org/wiki/PPU_nametables
Example:
    nametable[0] = 5
    top-left 8x8 background tile uses pattern tile #5

Responsibilities:
    chr_decoder.py => decodes CHR bytes into tile color indexes
    nametable_renderer.py => places decoded tiles according to nametable tile IDs
    framebuffer.py => stores RGB pixels

Simplification:
    Real NES nametable memory has:
    960 bytes tile IDs
    64 bytes attribute table
    - We will use only 960 visible tile bytes
    - We will use only one 4-color palette for every tile

Simplified step by step operative:
    nametable_byte <= tile_id
    decoded_tiles[tile_id] <= tile_data
    palette[color_index] <= tile_data[pixel]
    framebuffer[position] <= color_pixel

"""

from emulator.ppu.chr_decoder import CHR_TILE_HEIGHT, CHR_TILE_WIDTH, decode_pattern_table
from emulator.rendering.framebuffer import Framebuffer, RGBColor

NAMETABLE_ROWS = 30
NAMETABLE_TILES_PER_ROW = 32
NAMETABLE_SIZE = NAMETABLE_TILES_PER_ROW * NAMETABLE_ROWS

BACKGROUND_WIDTH = NAMETABLE_TILES_PER_ROW * CHR_TILE_WIDTH
BACKGROUND_HEIGHT = NAMETABLE_ROWS * CHR_TILE_HEIGHT

def nametable_to_framebuffer(
    nametable_bytes: bytes,
    pattern_table_bytes: bytes,
    palette: list[RGBColor],
) -> Framebuffer:
    if len(nametable_bytes) != NAMETABLE_SIZE:
        raise ValueError("Nametable visible tile area must be 960 bytes")

    decoded_tiles = decode_pattern_table(pattern_table_bytes)

    framebuffer = Framebuffer(
        width=BACKGROUND_WIDTH,
        height=BACKGROUND_HEIGHT
    )
    
    for tile_y in range(NAMETABLE_ROWS):
        for tile_x in range(NAMETABLE_TILES_PER_ROW):
            # For each background tile decode the tile pixels
            nametable_index = tile_y * NAMETABLE_TILES_PER_ROW + tile_x
            tile_id = nametable_bytes[nametable_index]
            tile = decoded_tiles[tile_id]

            for row in range(CHR_TILE_HEIGHT):
                for col in range(CHR_TILE_WIDTH):
                    # Select color for each pixel in tile
                    color_index = tile[row][col]
                    rgb = palette[color_index]
                    
                    # Paste color in framebuffer
                    pixel_x = tile_x * CHR_TILE_WIDTH + col
                    pixel_y = tile_y * CHR_TILE_HEIGHT + row
                    framebuffer.set_pixel(pixel_x, pixel_y, rgb)

    return framebuffer

