from dataclasses import dataclass, field


@dataclass
class RAM:
    _data: bytearray = field(default_factory=lambda: bytearray(0x800), init=False)
    
    def write(self, addr: int, value: int) -> None:
        """Write a value to internal ram"""
        self._memory[addr] = value

    def read(self, addr: int) -> int:
        """Get a value from internal ram"""
        return self._memory[addr]
