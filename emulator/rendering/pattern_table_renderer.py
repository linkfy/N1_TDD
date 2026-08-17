from emulator.ppu.chr_decoder import build_pattern_table_debug_grid, decode_pattern_table
from emulator.rendering.color_index_renderer import color_index_grid_to_framebuffer
from emulator.rendering.framebuffer import Framebuffer, RGBColor


def pattern_table_to_framebuffer(
    pattern_table_bytes: bytes,
    palette: list[RGBColor],
) -> Framebuffer:
    decoded_tiles = decode_pattern_table(pattern_table_bytes)
    grid = build_pattern_table_debug_grid(decoded_tiles)
    return color_index_grid_to_framebuffer(grid, palette)
