"""
PPU internal registers

yyy NN YYYYY XXXXX
||| || ||||| +++++-- coarse X scroll
||| || +++++-------- coarse Y scroll
||| ++-------------- nametable select
+++----------------- fine Y scroll
"""

from emulator.rendering.framebuffer import Framebuffer
from emulator.rendering.nametable_renderer import BackgroundOpaqueMask

NAMETABLE_PIXEL_WIDTH = 256
NAMETABLE_PIXEL_HEIGHT = 240
TILE_PIXEL_SIZE = 8

# Involved internal registers:
# vram_addr:            v => NO
# temp_vram_addr:       t => YES 
# fine_x:               x => YES
# second_write_toggle   w => NO
# -----------------------------
# Current simplified snapshot uses t and x
# Real hardware rendering uses v and x after timed t -> v transfers
BackgroundViewportPosition = tuple[int, int]
def decode_background_viewport_position(
        temp_vram_addr: int, 
        fine_x: int,
) -> BackgroundViewportPosition:
    coarse_x = temp_vram_addr & 0b1_1111
    coarse_y = (temp_vram_addr >> 5) & 0b1_1111

    nametable_x = (temp_vram_addr >> 10) & 1
    nametable_y = (temp_vram_addr >> 11) & 1

    fine_y = (temp_vram_addr >> 12) & 0b111

    viewport_x = (
        nametable_x * NAMETABLE_PIXEL_WIDTH
        + coarse_x * TILE_PIXEL_SIZE
        + fine_x
    )

    viewport_y = (
        nametable_y * NAMETABLE_PIXEL_HEIGHT
        + coarse_y * TILE_PIXEL_SIZE
        + fine_y
    )

    return viewport_x, viewport_y

def compose_horizontal_framebuffer_viewport(
        left: Framebuffer,
        right: Framebuffer,
        viewport_x: int,
) -> Framebuffer:

    expected_size = (
        NAMETABLE_PIXEL_WIDTH,
        NAMETABLE_PIXEL_HEIGHT,
    )
    
    if (left.width, left.height) != expected_size:
        raise ValueError(f"Left nametable framebuffer must be {expected_size[0]}x{expected_size[1]}")
    
    if (right.width, right.height) != expected_size:
        raise ValueError(f"Right nametable framebuffer must be {expected_size[0]}x{expected_size[1]}")

    logical_width = NAMETABLE_PIXEL_WIDTH * 2

    result = Framebuffer(
        width=NAMETABLE_PIXEL_WIDTH,
        height=NAMETABLE_PIXEL_HEIGHT,
    )

    for screen_y in range(NAMETABLE_PIXEL_HEIGHT):
        for screen_x in range(NAMETABLE_PIXEL_WIDTH):
            logical_x = (viewport_x + screen_x) % logical_width

            if logical_x < NAMETABLE_PIXEL_WIDTH:
                source = left
                source_x = logical_x
            else:
                source = right
                source_x = logical_x - NAMETABLE_PIXEL_WIDTH

            color = source.get_pixel(source_x, screen_y)
            result.set_pixel(screen_x, screen_y, color)
    return result


def compose_horizontal_opaque_mask_viewport(
        left: BackgroundOpaqueMask,
        right: BackgroundOpaqueMask,
        viewport_x: int,
) -> BackgroundOpaqueMask:
    
    expected_size = NAMETABLE_PIXEL_WIDTH * NAMETABLE_PIXEL_HEIGHT
    
    if len(left) != expected_size:
        raise ValueError(
                f"Left background opacity mask must contain {expected_size} entries"
        )

    if len(right) != expected_size:
        raise ValueError(
                f"Right background opacity mask must contain {expected_size} entries"
        )
    
    logical_width = NAMETABLE_PIXEL_WIDTH * 2
    result = [False] * expected_size

    for screen_y in range(NAMETABLE_PIXEL_HEIGHT):
        row_start = screen_y * NAMETABLE_PIXEL_WIDTH

        for screen_x in range(NAMETABLE_PIXEL_WIDTH):
            logical_x = (viewport_x + screen_x) % logical_width

            if logical_x < NAMETABLE_PIXEL_WIDTH:
                source = left
                source_x = logical_x
            else:
                source = right
                source_x = logical_x - NAMETABLE_PIXEL_WIDTH

            destination_index = row_start + screen_x
            source_index = row_start + source_x

            result[destination_index] = source[source_index]

    return result
