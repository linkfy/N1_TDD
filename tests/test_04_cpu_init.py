"""
Create the basic CPU Class
CPU Class should have one bus as a contrusctor parameter CPU(cpu_bus)

https://www.nesdev.org/wiki/CPU_registers
"""
import pytest
from emulator.bus.cpu_bus import CpuBus
from emulator.cpu.cpu import CPU


@pytest.fixture(scope="session")
def cpu():
    bus = CpuBus()
    default_cpu = CPU(bus)
    return default_cpu

def test_cpu_can_be_created():
    bus = CpuBus()
    cpu = CPU(bus)
    assert cpu.bus is bus

def test_cpu_has_registers(cpu):
    assert hasattr(cpu, "a") # Accumulator register
    assert hasattr(cpu, "x") # Index register X
    assert hasattr(cpu, "y") # Index register Y
    assert hasattr(cpu, "pc") # program counter
    assert hasattr(cpu, "s") # stack register
    assert hasattr(cpu, "p") # status register (Flags)

def test_cpu_registers_are_initialized(cpu):
    """ Initial register values
    https://www.nesdev.org/wiki/CPU_power_up_state
    """
    assert (cpu.a, cpu.x, cpu.y, cpu.pc, cpu.s, cpu.p) == (0, 0, 0, 0xFFFC, 0xFD, 0)

def test_cpu_fetch_byte(cpu):
    cpu.pc = 0 # Temporal PC value for testing
    """Get current value from register PC and then pc+=1"""
    cpu.bus.write(0x0000, 0x42)

    value = cpu.fetch_byte()

    assert value == 0x42
    assert cpu.pc == 1


def test_cpu_fetch_word(cpu):
    cpu.pc = 0 # Temporal PC value for testing
    cpu.bus.write(0x0000, 0x34)
    cpu.bus.write(0x0001, 0x12) # Write 0x34 , 0x12 (Little endian 0x1234)

    assert cpu.fetch_word() == 0x1234

    
def test_cpu_reads_reset_vector():
    """
    CPU Starts with reset -> JMP 0xFFFC
    Then it fetches a word -> 0xFFFC + 0xFFFD (00, 80)
    The fetched word contains 0x8000 (PC Start address)
    """
