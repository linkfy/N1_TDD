from dataclasses import dataclass, field

RGBColor = tuple[int, int, int]

NES_SCREEN_WIDTH = 256
NES_SCREEN_HEIGHT = 240
BLACK: RGBColor = (0, 0, 0)

@dataclass
class Framebuffer:
    width: int = NES_SCREEN_WIDTH
    height: int = NES_SCREEN_HEIGHT
    pixels: list[RGBColor] = field(default_factory=list)

    def __post_init__(self) -> None:
        if not self.pixels:
            self.pixels = [BLACK] * (self.width * self.height)

        if len(self.pixels) != self.width * self.height:
            raise ValueError("Framebuffer pixel count must be equal width * height")

    def get_pixel(self, x: int, y: int) -> RGBColor:
        return self.pixels[y * self.width + x]

    def set_pixel(self, x: int, y: int, color: RGBColor) -> None:
        self.pixels[y * self.width + x] = color
