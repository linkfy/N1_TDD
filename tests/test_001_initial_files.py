"""This tests ensures that initial files exists"""

from pathlib import Path


# CPU Folder files
def test_cpu_file_exists():
    assert Path("emulator/cpu/cpu.py").exists()


def test_cpu_addressing_mode_file_exists():
    assert Path("emulator/cpu/addressing_modes.py").exists()


def test_cpu_instructions_file_exists():
    assert Path("emulator/cpu/instructions.py").exists()


# BUS Folder files
def test_cpu_bus_file_exists():
    assert Path("emulator/bus/cpu_bus.py").exists()


# Memory Files
def test_memory_ram_file_exists():
    assert Path("emulator/memory/ram.py").exists()
