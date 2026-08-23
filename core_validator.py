from pathlib import Path

from emulator.bus.cpu_bus import CpuBus
from emulator.cartridge.cartridge import Cartridge
from emulator.console import Console
from emulator.cpu.cpu import CPU


ROM_PATH = Path("MarioBros.nes")
debug_mode = True

def main() -> None:
    if not ROM_PATH.exists():
        raise FileNotFoundError(
            "MarioBros.nes not found. Provide your own legal local copy. "
            "This file is intentionally not included in the tutorial repository."
        )

    cartridge = Cartridge.from_ines_bytes(ROM_PATH.read_bytes())

    cpu_bus = CpuBus(cartridge=cartridge)
    cpu = CPU(cpu_bus)
    console = Console(cpu=cpu, ppu=cpu_bus.ppu)
    
    cpu.reset()
    
    print(f"Loaded {ROM_PATH}")
    print(f"CPU reset PC = ${cpu.pc:04X}")
    print("Starting frame loop. Press Ctrl+C to stop.")
    
    try:
        while True:
            executed = console.step_until_next_frame()
            if debug_mode:
                print(f"frame={console.ppu.frame} pc=${cpu.pc:04X} instructions={executed}") 
    except KeyboardInterrupt:
        print("\nStopped by user.")


if __name__ == "__main__":
    main()
