from dataclasses import dataclass, field

from emulator.memory.memory_device import MemoryDevice


@dataclass
class ROM(MemoryDevice):
    _data: bytes
    
    def write(self, addr: int, value: int) -> None:
        raise ValueError("Cannot write to ROM")

    def read(self, addr: int) -> int:
        """Get a value from internal ROM"""
        return self._data[addr]
