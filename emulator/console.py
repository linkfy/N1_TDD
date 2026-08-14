from dataclasses import dataclass

from emulator.cpu.cpu import CPU
from emulator.ppu.ppu import PPU

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

