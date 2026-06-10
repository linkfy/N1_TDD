from abc import ABC, abstractmethod

class MemoryDevice(ABC):
    @abstractmethod
    def read(self, addr: int) -> int:
        ...
    
    @abstractmethod
    def write(self, addr: int, value: int) -> None:
        ...
