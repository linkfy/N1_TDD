from dataclasses import dataclass, field
from emulator.memory.memory_device import MemoryDevice

VRAM_SIZE = 0x4000

@dataclass
class VRAM(MemoryDevice):
    _data: bytearray = field(default_factory=lambda: bytearray(VRAM_SIZE), init=False)
    
    def write(self, addr: int, value: int) -> None:
        """Write a value to internal vram"""
        self._data[addr] = value & 0xFF

    def read(self, addr: int) -> int:
        """Get a value from internal vram"""
        return self._data[addr]
