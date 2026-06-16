from emulator.cpu.cpu import CPU
from emulator.bus.cpu_bus import CpuBus
from emulator.memory.fake_rom import FakeROM


def test_lda_opcode():
    """This is yout first opcode resoultion.
    You should define a step function inside CPU
    cpu.step() and implement opcode LDA 0xA9
    It should: 
        - Fetch opcode [fetch_byte]
        - Decode opcode [if opcode == 0xA9 ... then ... return]
        - raise NotImplementedError if Opcode Not Implemented
    
    Baby steps:
    
    def step(self) -> None:
        opcode = self.fetch_byte()

        if opcode == 0xA9
            self.a = self.fetch_byte()
            return
        raise NotImplementedError(f"{opcode:02X} not implemented")

    LDA Reference:
    https://www.nesdev.org/wiki/Instruction_reference#LDA
    """
    
    # Current flow CPU Status: Reset -> Fetch -> Decode
    rom = FakeROM()
    
    # Reset Vector
    rom.write(0x7FFC, 0x00)
    rom.write(0x7FFD, 0x80)

    # LDA #$42
    rom.write(0x0000, 0xA9)
    rom.write(0x0001, 0x42)

    bus = CpuBus(program_rom=rom)
    cpu = CPU(bus)

    cpu.reset()
    cpu.step() # LDA should fetch_byte and put it on register A

    assert cpu.a == 0x42


