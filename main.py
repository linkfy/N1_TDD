from pathlib import Path

import pygame

from emulator.bus.cpu_bus import CpuBus
from emulator.cartridge.cartridge import Cartridge
from emulator.console import Console
from emulator.cpu.cpu import CPU
from emulator.input.controller import Controller
from tools.show_framebuffer import draw_framebuffer

ROM_PATH = Path("MarioBros.nes")
debug_mode = False
SCALE = 3

KEYS = {
    "a": pygame.K_z,
    "b": pygame.K_x,
    "select": pygame.K_RSHIFT,
    "start": pygame.K_RETURN,
    "up": pygame.K_UP,
    "down": pygame.K_DOWN,
    "left": pygame.K_LEFT, 
    "right": pygame.K_RIGHT, 
}

def handle_key_event(controller: Controller, key: int, pressed: bool) -> None:
    if key == KEYS["a"]:
        controller.a = pressed
    elif key == KEYS["b"]:
        controller.b = pressed
    elif key == KEYS["select"]:
        controller.select = pressed
    elif key == KEYS["start"]:
        controller.start = pressed
    elif key == KEYS["up"]:
        controller.up = pressed
    elif key == KEYS["down"]:
        controller.down = pressed
    elif key == KEYS["left"]:
        controller.left = pressed
    elif key == KEYS["right"]:
        controller.right = pressed

def print_emulation_error(error: Exception, console: Console) -> None:
    print("\nEmulation Error:")
    print(f"    type={type(error).__name__}")
    print(f"    message={error}")
    print(f"    pc=${console.cpu.pc:04X}")
    print(f"    ppu_frame={console.ppu.frame}")
    print(f"    ppu_scanline={console.ppu.scanline}")
    print(f"    ppu_cycle={console.ppu.cycle}")


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
    framebuffer = console.render_background_framebuffer()
    print(f"Loaded {ROM_PATH}")
    print(f"CPU reset PC = ${cpu.pc:04X}")
    print("Starting frame loop. Press Ctrl+C to stop.")
    
    pygame.init()
    try:
        window = pygame.display.set_mode(
            (framebuffer.width * SCALE, framebuffer.height * SCALE)
        )
        pygame.display.set_caption("NES Background")
        
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    handle_key_event(cpu_bus.controller_1, event.key, True)
                elif event.type == pygame.KEYUP:
                    handle_key_event(cpu_bus.controller_1, event.key, False)

            executed = console.step_until_next_frame()
            framebuffer = console.render_background_framebuffer()
            draw_framebuffer(window, framebuffer, SCALE)
            pygame.display.flip()

            if debug_mode:
                print(f"frame={console.ppu.frame} pc=${cpu.pc:04X} instructions={executed}") 

    except KeyboardInterrupt:
        print("\nStopped by user.")
    except Exception as error:
                print_emulation_error(error, console)
                raise
    finally:
        pygame.quit()


if __name__ == "__main__":
    main()
