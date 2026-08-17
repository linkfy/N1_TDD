"""from emulator.bus.cpu_bus import CpuBus
from emulator.cartridge.cartridge import Cartridge
from emulator.console import Console
from emulator.cpu.cpu import CPU
from emulator.ppu.ppu import PPU


def main():
    print("Hello from nes-1!")
    nesfile = open("MarioBros.nes", "rb").read()
    cartridge = Cartridge.from_ines_bytes(nesfile)
    cpu_bus = CpuBus(cartridge=cartridge)
    cpu = CPU(cpu_bus)
    ppu = PPU()
    console = Console(cpu, ppu)
    print("Starting")
    while True:
        cycles = console.step()
        print(cycles)


if __name__ == "__main__":
    main()
"""
