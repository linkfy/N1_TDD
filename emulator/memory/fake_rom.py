from dataclasses import dataclass, field

from emulator.memory.memory_device import MemoryDevice

@dataclass
class FakeROM(MemoryDevice):

    _data: bytearray = field(default_factory=lambda: bytearray(0x8000), init=False)
    
    def write(self, addr: int, value: int) -> None:
        """Write a value to Fake ROM
        Remember: in a Real ROM, This should not be possible
        For testing purposes
        """
        self._data[addr] = value

    def read(self, addr: int) -> int:
        """Read a value from Fake ROM
        """
        return self._data[addr]
