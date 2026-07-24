"""
Add optional Cartridge support to CpuBus, part 1.

File to update:
    emulator/bus/cpu_bus.py

What this part implements:
    - CpuBus accepts an optional cartridge
    - CpuBus creates a mapper from that cartridge in __post_init__
    - CpuBus rejects attaching both program_rom and cartridge

What this part does NOT implement yet:
    - CPU reads from cartridge PRG ROM

That read behavior is tested in part 2.

Why split this into two parts:
Adding cartridge support has two separate responsibilities:

    1. construction-time wiring
    2. read-time routing

Keeping them separate makes the tutorial easier to follow. Students first learn
how the bus receives a cartridge and turns it into a mapper. Only after that do
they change the read path for $8000-$FFFF.

Architecture model:

    Cartridge
        stores PRG ROM, CHR ROM, and mapper number

    create_mapper(cartridge)
        chooses the correct mapper implementation

    Mapper000
        translates CPU PRG addresses into PRG ROM offsets

    CpuBus
        owns routing decisions

Important boundary:
CpuBus should not implement Mapper000 mirroring rules directly. It should create
or hold a mapper, then later delegate PRG reads to mapper.read_prg(addr).

Expected implementation shape:

    @dataclass
    class CpuBus:
        program_rom: Optional[MemoryDevice] = None
        cartridge: Optional[Cartridge] = None
        ram: RAM = field(default_factory=RAM)

        def __post_init__(self):
            if self.program_rom is not None and self.cartridge is not None:
                raise ValueError("Cannot attach both program_rom and cartridge")

            self.mapper = None

            if self.cartridge is not None:
                self.mapper = create_mapper(self.cartridge)

Read-path reminder:
Do not change the $8000-$FFFF read behavior in this part unless you are already
working ahead. Part 2 will guide that exact change.
"""

import dataclasses

import pytest

from emulator.bus.cpu_bus import CpuBus
from emulator.cartridge.cartridge import Cartridge
from emulator.cartridge.mapper000 import CHR_ROM_SIZE, Mapper000, NROM_128_SIZE
from emulator.memory.fake_rom import FakeROM


def make_nrom_cartridge() -> Cartridge:
    """Create a minimal Mapper000-compatible cartridge."""
    return Cartridge(
        prg_rom=bytes([0xEA]) * NROM_128_SIZE,
        chr_rom=bytes([0x00]) * CHR_ROM_SIZE,
        mapper_number=0,
    )


def test_cpu_bus_has_optional_cartridge_field():
    """
    Objective:
    Add cartridge as an optional CpuBus field.

    Why:
    Earlier CPU tests used program_rom=FakeROM for convenience. Real ROM loading
    should now be able to connect a Cartridge without removing the old test path.
    """
    assert dataclasses.is_dataclass(CpuBus)
    assert "cartridge" in CpuBus.__dataclass_fields__


def test_cpu_bus_defines_post_init_for_cartridge_wiring():
    """
    Objective:
    CpuBus should have __post_init__.

    Why:
    Dataclass construction gives us the raw fields. __post_init__ is the right
    place to validate invalid combinations and create derived wiring such as the
    mapper created from the cartridge.
    """
    assert hasattr(CpuBus, "__post_init__")
    assert callable(CpuBus.__post_init__)


def test_cpu_bus_rejects_program_rom_and_cartridge_together():
    """
    Objective:
    Avoid ambiguous PRG ROM sources.

    Why:
    If both program_rom and cartridge are attached, the bus would have two
    possible sources for $8000-$FFFF. Silent priority rules make emulator bugs
    hard to debug, so the bus should fail loudly.
    """
    with pytest.raises(ValueError):
        CpuBus(program_rom=FakeROM(), cartridge=make_nrom_cartridge())


def test_cpu_bus_creates_mapper_from_cartridge():
    """
    Objective:
    When a cartridge is attached, CpuBus should create the mapper through the
    mapper factory.

    Important:
    This test checks construction-time wiring only. It does not check CPU reads
    yet. Part 2 will verify that $8000-$FFFF delegates to mapper.read_prg(addr).
    """
    cartridge = make_nrom_cartridge()

    bus = CpuBus(cartridge=cartridge)

    assert isinstance(bus.mapper, Mapper000)
    assert bus.mapper.prg_rom == cartridge.prg_rom
    assert bus.mapper.chr_rom == cartridge.chr_rom
