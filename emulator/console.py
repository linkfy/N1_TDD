from dataclasses import dataclass

from emulator.cpu.cpu import CPU
from emulator.ppu.ppu import PPU

from emulator.rendering.framebuffer import Framebuffer
from emulator.rendering.ppu_background_renderer import ppu_background_to_framebuffer

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
