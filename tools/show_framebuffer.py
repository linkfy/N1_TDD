"""
Manual framebuffer display helpers.
This module is intentionally outside core.

Core modules rendering | ppu | console must not depend on pygame
"""
import warnings
import pygame
from emulator.rendering.framebuffer import Framebuffer

SCALE = 3

"""
Draw Checkerboard to framebuffer:
 __________________   
| []  []  []  []  |
|   []  []  []  []|
| []  []  []  []  |
|   []  []  []  []|
| []  []  []  []  |
|   []  []  []  []|
 -----------------
"""
def make_checkerboard_framebuffer(width: int = 64, height: int = 64) -> Framebuffer:
    """Create a synthetic checkerboard framebuffer for manual display tests.""" 
    framebuffer = Framebuffer(width=width, height=height)

    for y in range(height):
        for x in range(width):
            block_x = x // 8
            block_y = y // 8

            if (block_x + block_y) % 2 == 0:
                framebuffer.set_pixel(x, y, (255, 255, 255))
            else:
                framebuffer.set_pixel(x, y, (40, 40, 40))
    return framebuffer

def old_draw_framebuffer(
        surface: pygame.Surface,
        framebuffer: Framebuffer,
        scale: int
) -> None:
    #Write the framebuffer to pygame surface

    for y in range(framebuffer.height):
        for x in range(framebuffer.width):
            color = framebuffer.get_pixel(x, y)
            
            rect = pygame.Rect(
                x * scale,
                y * scale,
                scale,
                scale,
            )

            surface.fill(color, rect)

def draw_framebuffer(
        surface: pygame.Surface,
        framebuffer: Framebuffer,
        scale: int
) -> None:
    """Write the framebuffer to pygame surface using one image upload"""

    rgb_bytes = bytearray(framebuffer.width * framebuffer.height * 3)

    write_index = 0
    for color in framebuffer.pixels:
        red, green, blue = color
        rgb_bytes[write_index] = red
        rgb_bytes[write_index + 1] = green
        rgb_bytes[write_index + 2] = blue
        write_index += 3

    frame_surface = pygame.image.frombuffer(
        bytes(rgb_bytes),
        (framebuffer.width, framebuffer.height),
        "RGB",
    )

    if scale == 1:
        surface.blit(frame_surface, (0, 0))
        return

    scaled_surface = pygame.transform.scale(
        frame_surface,
        (framebuffer.width * scale, framebuffer.height * scale),
    )
    
    surface.blit(scaled_surface, (0,0))

def main() -> None:
    """Open a pygame window and display a synthetic Framebuffer"""
    
    framebuffer = make_checkerboard_framebuffer()

    pygame.init()
    try:
        window = pygame.display.set_mode(
            (framebuffer.width * SCALE, framebuffer.height * SCALE)
        )
        pygame.display.set_caption("Framebuffer Smoke Test")

        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            draw_framebuffer(window, framebuffer, SCALE)
            pygame.display.flip()
    finally:
        pygame.quit()

if __name__ == "__main__":
    main()
