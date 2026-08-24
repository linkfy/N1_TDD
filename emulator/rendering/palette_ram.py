"""
Backgrounds and sprites are located at $3F00-$3F1F in VRAM (32 Bytes)
$3F00-$3F0F -> background palettes (4)
$3F10-$3F1F -> sprites palettes (4)
For sprites entry 0 is unused, transparent.
For backgrounds color index 0 uses shared backdrop/universal background color. [First palette_ram byte]
We have a total of 4 background palettes
https://www.nesdev.org/wiki/PPU_palettes#Palette_RAM
"""
from emulator.rendering.framebuffer import RGBColor
from emulator.rendering.nes_palette import get_nes_rgb_color


PALETTE_RAM_SIZE = 16
TOTAL_PALETTES = 4
COLORS_PER_PALETTE = 4

BackgroundPalettes = list[list[RGBColor]]
def build_background_palettes_from_palette_ram(
    palette_ram: bytes,
) -> BackgroundPalettes:
    if len(palette_ram) != PALETTE_RAM_SIZE:
        raise ValueError(f"Background palette RAM must be {PALETTE_RAM_SIZE} bytes")

    # Color used by default behind both, background and sprites
    backdrop_color = get_nes_rgb_color(palette_ram[0])
    
    background_palettes = []
    
    for palette_id in range(TOTAL_PALETTES):
        base = palette_id * COLORS_PER_PALETTE
    
        palette = [
            backdrop_color,
            get_nes_rgb_color(palette_ram[base + 1]),
            get_nes_rgb_color(palette_ram[base + 2]),
            get_nes_rgb_color(palette_ram[base + 3]),
        ]

        background_palettes.append(palette)

    return background_palettes

SpritePalettes = list[list[RGBColor]]
def build_sprite_palettes_from_palette_ram(palette_ram: bytes) -> SpritePalettes:
    if len(palette_ram) != PALETTE_RAM_SIZE:
        raise ValueError(f"Sprite palette RAM must be {PALETTE_RAM_SIZE} bytes")

    sprite_palettes = []

    for palette_id in range(TOTAL_PALETTES):
        base = palette_id * COLORS_PER_PALETTE
    
        palette = [
            get_nes_rgb_color(palette_ram[base]),
            get_nes_rgb_color(palette_ram[base + 1]),
            get_nes_rgb_color(palette_ram[base + 2]),
            get_nes_rgb_color(palette_ram[base + 3]),
        ]

        sprite_palettes.append(palette)

    return sprite_palettes



