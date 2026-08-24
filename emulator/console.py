from dataclasses import dataclass

from emulator.cpu.cpu import CPU
from emulator.ppu.ppu import CTRL_SPRITE_PATTERN_TABLE, PPU
from emulator.bus.ppu_bus import PALETTE_START

from emulator.rendering.frame_compositor import composite_background_and_sprites
from emulator.rendering.framebuffer import Framebuffer
from emulator.rendering.palette_ram import build_sprite_palettes_from_palette_ram
from emulator.rendering.ppu_background_renderer import (
    ppu_background_to_framebuffer,
    ppu_background_to_opaque_mask,
    PATTERN_TABLE_0_ADDR, 
    PATTERN_TABLE_1_ADDR
)

@dataclass
class Console:
    cpu: CPU
    ppu: PPU

    def consume_nmi_if_requested(self) -> None:
        if not self.ppu.nmi_requested:
            return

        self.ppu.nmi_requested = False
        self.cpu.interrupt_nmi()

    def step(self) -> int:
        # Accurate approach needs:
        # - branch taken extra cycles
        # - NMI Latency
        # - DMA stalls
        cpu_cycles = self.cpu.step()
        self.ppu.step(cpu_cycles * 3)
        self.consume_nmi_if_requested()
        return cpu_cycles

    def step_until_next_frame(self, max_cpu_instructions: int | None = None) -> int:
        start_frame = self.ppu.frame
        executed = 0

        while self.ppu.frame == start_frame:
            if max_cpu_instructions is not None:
                if executed >= max_cpu_instructions:
                    raise RuntimeError("Frame did not complete before instruction limit")
            self.step()
            executed += 1
        return executed

    def render_background_framebuffer(self) -> Framebuffer:
        return ppu_background_to_framebuffer(self.ppu)

    def render_framebuffer(self) -> Framebuffer:
        background = self.render_background_framebuffer()
        background_opaque_mask = ppu_background_to_opaque_mask(self.ppu)
        
        # Select sprite area from palette_ram is 16 bytes after background palette area
        sprite_palette_start = PALETTE_START + 16
        
        sprite_palette_ram = bytes(
            self.ppu.ppu_bus.read(sprite_palette_start + offset)
            for offset in range(16)
        )

        sprite_palettes = build_sprite_palettes_from_palette_ram(sprite_palette_ram)

        pattern_table_base = (PATTERN_TABLE_1_ADDR  
                              if self.ppu.ctrl & CTRL_SPRITE_PATTERN_TABLE else PATTERN_TABLE_0_ADDR)
        

        pattern_table = bytes(
            self.ppu.ppu_bus.read(pattern_table_base + offset)
            for offset in range(0x1000) # Pattern Table size
        )
        
        return composite_background_and_sprites(
            background=background,
            oam=self.ppu.oam,
            pattern_table=pattern_table,
            sprite_palettes=sprite_palettes,
            background_opaque_mask=background_opaque_mask,
        )
