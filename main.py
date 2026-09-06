from pathlib import Path

import pygame
import time

from emulator.bus.cpu_bus import CpuBus
from emulator.cartridge.cartridge import Cartridge
from emulator.console import Console
from emulator.cpu.cpu import CPU
from emulator.input.controller import Controller
from tools.show_framebuffer import draw_framebuffer
# OLD TEST GAME First Mario Bros
# ROM_PATH = Path("MarioBros.nes")
# NEW TEST GAME Super Mario Bros
ROM_PATH = Path("/home/linkfy/Downloads/SMB.nes")

debug_mode = False
SCALE = 3
FPS_REPORT_INTERVAL_SECONDS = 1.0

TARGET_DISPLAY_FPS = 60
TARGET_FRAME_SECONDS = 1.0 / TARGET_DISPLAY_FPS


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
    framebuffer = console.render_framebuffer()
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
        next_frame_deadline = time.perf_counter() + TARGET_FRAME_SECONDS
        last_fps_report_time = time.perf_counter()
        frames_since_last_report = 0
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    handle_key_event(cpu_bus.controller_1, event.key, True)
                elif event.type == pygame.KEYUP:
                    handle_key_event(cpu_bus.controller_1, event.key, False)

            executed = console.step_until_next_frame()
            framebuffer = console.render_framebuffer()
            draw_framebuffer(window, framebuffer, SCALE)
            pygame.display.flip()

            # Prevent accumulated timing drift: absolute-deadline frame pacing
            # Explained with example
            # 1) Loop waits until time is next_frame_deadline 
            # Imagine that we finish at 14ms, then we wait until 16.67
            while time.perf_counter() < next_frame_deadline:
                pass
            # 2) When we reach 16.67ms deadline, add 16.67 more => 33.34
            # Every deadline remains exactly one frame period:
            now = time.perf_counter()
            next_frame_deadline += TARGET_FRAME_SECONDS

            # Suppose current deadline is 50ms + 16.67 => 66.67
            # and we finish at 90ms
            # 90 - 66.67 = 23.33 ms late
            # It is more than one complete frame period,
            # We need to calculate again for those cases
            if now - next_frame_deadline >= TARGET_FRAME_SECONDS:
                # Next iteration is actual time + 16.67ms
                next_frame_deadline = now + TARGET_FRAME_SECONDS

            # Show FPS 
            frames_since_last_report += 1
            now = time.perf_counter()
            elapsed = now - last_fps_report_time

            if elapsed >= FPS_REPORT_INTERVAL_SECONDS:
                fps = frames_since_last_report / elapsed
                print(f"fps={fps:.1f}")
                frames_since_last_report = 0
                last_fps_report_time = now
                
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
