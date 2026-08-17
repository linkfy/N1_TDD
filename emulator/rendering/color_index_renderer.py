"""
A color-index grid is a 2D grid where each number is an index into a palette

grid = [
    [0, 1, 2, ...],
    [2, 3, 3, ...],
    ...
]

palette = [
    (0, 0, 0),
    (11, 11, 11),
    (22, 22, 22),
    (255, 255, 255),
]
"""

from emulator.rendering.framebuffer import Framebuffer, RGBColor

Grid = list[list[int]]

def color_index_grid_to_framebuffer(
    grid: Grid,
    palette: list[RGBColor] 
) -> Framebuffer:

    height = len(grid)
    width = len(grid[0])

    framebuffer = Framebuffer(width=width, height=height)

    for y, row in enumerate(grid):
        for x, color_index in enumerate(row):
            framebuffer.set_pixel(x, y, palette[color_index])

    return framebuffer
