from emulator.rendering.framebuffer import Framebuffer
from emulator.rendering.nametable_renderer import BackgroundOpaqueMask
from emulator.rendering.palette_ram import SpritePalettes
from emulator.rendering.sprite_renderer import render_oam_sprites_to_framebuffer

def composite_background_and_sprites(
    background: Framebuffer,
    oam: bytes | bytearray,
    pattern_table: bytes,
    sprite_palettes: SpritePalettes,
    background_opaque_mask: BackgroundOpaqueMask | None = None,
) -> Framebuffer:

    framebuffer = Framebuffer(
        width=background.width,
        height=background.height,
        pixels=list(background.pixels),
    )

    render_oam_sprites_to_framebuffer(
        framebuffer,
        oam,
        pattern_table,
        sprite_palettes,
        background_opaque_mask,
    )

    return framebuffer
