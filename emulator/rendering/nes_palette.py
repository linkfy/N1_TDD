"""
    NES has hardware color generator
    Produces 64 colors from indexes $00-3F
    Analog circuit / signal generation produces the color
    Pixel Palette Entry -> PPU Palette RAM Index -> Analog circuit turns to Color to video signal
"""

from emulator.rendering.framebuffer import RGBColor

NES_PALETTE_SIZE = 64
# This palette is obtained from https://www.nesdev.org/wiki/File:2C02G_U_wiki.pal
# It is color approximations, the file contains more than 64 normal colors, the extra entries are "emphasis" colors
# Not used for this emulator, this happens when PPUMASK writes to bits 5-7 for "emphasize"
# Bit 5 -> red, Bit 6 -> Green, Bit 7 -> Blue
"""
file = "2C02G_U_wiki.pal"
data = open(file, "rb").read()
for i in range(0, 64*3, 3):
         rgb = data[i:i+3]
         if len(rgb) == 3:
            r, g, b = rgb[0], rgb[1], rgb[2]
            print(f"({r},{g},{b}),")
"""
NES_PALETTE_RGB: list[RGBColor] = [

    (87,87,87),     (0,12,142),     (8,0,166),      (52,0,150),      (85,0,97),      (99,0,21),      (90,0,0),       (60,14,0),
    (17,40,0),      (0,59,0),       (0,66,0),       (0,58,5),        (0,38,82),      (0,0,0),        (0,0,0),        (0,0,0),
    
    (165,165,165),  (0,65,217),     (47,30,255),    (103,4,242),     (148,0,180),    (170,0,87),     (163,24,0),     (128,57,0),
    (75,91,0),      (19,118,0),     (0,129,0),      (0,121,35),      (0,98,136),     (0,0,0),        (0,0,0),        (0,0,0),

    (255,255,255),  (74,159,255),   (121,126,255),  (175,99,255),    (221,85,255),   (247,87,194),   (247,106,99),   (220,136,16),
    (174,169,0),    (120,196,0),    (74,210,17),    (47,207,100),    (47,189,196),   (65,65,65),     (0,0,0),        (0,0,0),

    (255,255,255),  (185,221,255),  (202,209,255),  (222,198,255),   (240,192,255),  (252,192,238),  (253,198,202),  (245,208,170),
    (228,221,149),  (208,232,146),  (189,238,162),  (178,238,192),   (176,232,227),  (179,179,179),  (0,0,0),        (0,0,0),
]

def get_nes_rgb_color(index: int) -> RGBColor:
    return NES_PALETTE_RGB[index & 0x3F]
