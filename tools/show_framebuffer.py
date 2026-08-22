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

def draw_framebuffer(
        surface: pygame.Surface,
        framebuffer: Framebuffer,
        scale: int
) -> None:
    """Write the framebuffer to pygame surface"""
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
