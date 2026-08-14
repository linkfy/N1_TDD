from dataclasses import dataclass, field

from emulator.bus.cpu_bus import CpuBus
from emulator.cpu.opcodes import OPCODE_CYCLES, OPCODE_TABLE
from emulator.cpu.flags_handler import FlagsHandler
from emulator.cpu.flags_handler import  (
        ZERO_FLAG, 
        INTERRUPT_FLAG,
        B_FLAG,
        ONE_FLAG,
        NEGATIVE_FLAG
)

NMI_VECTOR_LOW = 0xFFFA
NMI_VECTOR_HIGH = 0xFFFB

STACK_BASE = 0x0100

@dataclass
class CPU:
    bus: CpuBus
    flags: FlagsHandler = field(init=False)

    def __post_init__(self):
        self.flags = FlagsHandler(self)
    
    # Initial Registers with default value
    a: int = 0
    x: int = 0
    y: int = 0
    pc: int = 0
    s: int = 0
    p: int = 0

    def _update_zero_and_negative_flags(self, value: int):

        if value == 0:
            self.p |= ZERO_FLAG # Set Z
        else:
            self.p &= ~ZERO_FLAG # Unset Z
        
        if (value & NEGATIVE_FLAG) != 0: # Set N
            self.p |= NEGATIVE_FLAG
        else:
            self.p &= ~NEGATIVE_FLAG # Unset N

        return



    # Get one byte from bus and increment pc
    def fetch_byte(self) -> int:
        value = self.bus.read(self.pc)
        self.pc += 1
        return value

    def fetch_word(self) -> int:
        low = self.fetch_byte()
        high = self.fetch_byte()

        return low | (high << 8)

    def reset(self) -> None:
        """
        Read the reset vector stored at addresses
        0xFFFC and 0xFFFD and initialize the
        Program Counter.
        """
        self.s = 0xFD
        self.p = 0x04
        
        # PC = ($FFFC) -> Value inside address
        low = self.bus.read(0xFFFC)
        high = self.bus.read(0xFFFD)
        self.pc = low | (high << 8)


    def step(self) -> int:
        opcode = self.fetch_byte()
        handler = OPCODE_TABLE.get(opcode) # Returns None if not exists
        if handler is None:
            raise NotImplementedError(f"Opcode {opcode:02X} not implemented")
        
        handler(self)
        return OPCODE_CYCLES[opcode]
    
    
    def push_stack(self, value: int) -> None:
        self.bus.write(STACK_BASE | self.s, value & 0xFF)
        self.s = (self.s - 1) & 0xFF


    def pop_stack(self) -> int:
        self.s = (self.s + 1) & 0xFF
        return self.bus.read(STACK_BASE | self.s)

    def interrupt_nmi(self):
        # Push PC High and PC Low
        pc_high = (self.pc >>8) & 0xFF
        self.push_stack(pc_high)
        pc_low = self.pc & 0xFF
        self.push_stack(pc_low)
        
        # Push P on stack (with B flag *clear*)
        status_to_push = self.p | ONE_FLAG # Flag ONE is always set
        status_to_push &= ~B_FLAG
        self.push_stack(status_to_push)
        
        # Set I Flag
        self.p |= INTERRUPT_FLAG
        
        # Load new PC from NMI Vector
        low = self.bus.read(NMI_VECTOR_LOW)
        high = self.bus.read(NMI_VECTOR_HIGH)
        self.pc = (high << 8) | low
        




        
