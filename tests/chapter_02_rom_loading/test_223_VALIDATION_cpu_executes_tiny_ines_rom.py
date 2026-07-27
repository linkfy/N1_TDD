"""
VALIDATION TEST: CPU executes a tiny generated iNES ROM.

This is not a student implementation step.

There is nothing new for the student to build in this file. This test validates
that the pieces implemented in the previous chapter 02 steps work together:

    iNES bytes
        -> Cartridge.from_ines_bytes(data)
        -> CpuBus(cartridge=cartridge)
        -> create_mapper(cartridge)
        -> Mapper000
        -> CPU.reset()
        -> CPU.step()

Why this validation exists:
Unit tests can prove each part in isolation, but emulator bugs often appear at
boundaries. This test proves that the CPU can fetch and execute an instruction
from cartridge-backed PRG ROM using the reset vector.

The ROM is generated inside the test. It is intentionally tiny and does not use
PPU, APU, controllers, interrupts, or any feature outside the current emulator
scope.

Tiny program placed at CPU address $8000:

    A9 42    LDA #$42
    EA       NOP

Reset vector:

    CPU $FFFC = $00
    CPU $FFFD = $80

So after reset:

    PC = $8000

Important Mapper000 detail:
For a 16KB NROM cartridge, CPU $FFFC-$FFFD maps to PRG ROM offsets
$3FFC-$3FFD because $C000-$FFFF mirrors the 16KB PRG bank.
"""

from emulator.bus.cpu_bus import CpuBus
from emulator.cartridge.cartridge import Cartridge
from emulator.cartridge.ines import CHR_ROM_BANK_SIZE, PRG_ROM_BANK_SIZE
from emulator.cpu.cpu import CPU


def make_tiny_ines_rom() -> bytes:
    """Build a minimal Mapper000 iNES ROM entirely in memory."""
    header = bytearray(16)
    header[0:4] = b"NES\x1A"
    header[4] = 1  # one 16KB PRG ROM bank
    header[5] = 1  # one 8KB CHR ROM bank
    header[6] = 0x00  # mapper 0, no trainer
    header[7] = 0x00  # mapper 0

    prg_rom = bytearray(PRG_ROM_BANK_SIZE)
    prg_rom[0x0000] = 0xA9  # LDA immediate
    prg_rom[0x0001] = 0x42
    prg_rom[0x0002] = 0xEA  # NOP

    # Reset vector: CPU $FFFC-$FFFD -> PRG offsets $3FFC-$3FFD for 16KB NROM.
    prg_rom[0x3FFC] = 0x00
    prg_rom[0x3FFD] = 0x80

    chr_rom = bytes([0x00]) * CHR_ROM_BANK_SIZE

    return bytes(header) + bytes(prg_rom) + chr_rom


def test_cpu_executes_tiny_generated_ines_rom_from_reset_vector():
    """
    Validation objective:
    Prove that a tiny generated iNES ROM can be parsed, connected to CpuBus, and
    executed by CPU.step() after CPU.reset().
    """
    cartridge = Cartridge.from_ines_bytes(make_tiny_ines_rom())
    bus = CpuBus(cartridge=cartridge)
    cpu = CPU(bus=bus)

    cpu.reset()
    assert cpu.pc == 0x8000

    cpu.step()

    assert cpu.a == 0x42
    assert cpu.pc == 0x8002
