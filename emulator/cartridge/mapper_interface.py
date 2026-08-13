from typing import Protocol

class MapperInterface(Protocol):
    def read_prg(self, addr: int) -> int:
        ...

    def write_prg(self, addr: int, value: int) -> None:
        ...

    def read_chr(self, addr: int) -> int:
        ...

    def write_chr(self, addr: int, value: int) -> None:
        ...


