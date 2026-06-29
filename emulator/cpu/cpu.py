from dataclasses import dataclass

from emulator.bus.cpu_bus import CpuBus

@dataclass
class CPU:
    bus: CpuBus
    
    # Initial Registers with default value
    a: int = 0
    x: int = 0
    y: int = 0
    pc: int = 0
    s: int = 0
    p: int = 0

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

    def step(self) -> None:
        opcode = self.fetch_byte()

        if opcode == 0xA9: # LDA Inmediate
            self.a = self.fetch_byte()
            # Set Flags

            # Zero Flag
            if self.a == 0:
                self.p |= (1 << 1) # set flag Zero
            else:
                self.p &= ~(1 << 1) # unset flag Zero

            if (self.a & (1 << 7)) != 0: # bit 7 active, then is negative
                self.p |= (1 << 7)
            else:
                self.p &= ~(1 << 7) # bit 7 set to 0

            return
        elif opcode == 0xAD: # LDA Absolute
            addr = self.fetch_word()
            self.a = self.bus.read(addr)
            # Set Flags [Copy-pasted code from opcode 0xA9]

            # Zero Flag
            if self.a == 0:
                self.p |= (1 << 1) # set flag Zero
            else:
                self.p &= ~(1 << 1) # unset flag Zero

            if (self.a & (1 << 7)) != 0: # bit 7 active, then is negative
                self.p |= (1 << 7)
            else:
                self.p &= ~(1 << 7) # bit 7 set to 0

            return
            
        raise NotImplementedError(f"Opcode {opcode:02X} not implemented")
