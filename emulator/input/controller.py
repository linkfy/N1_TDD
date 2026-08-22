# https://www.nesdev.org/wiki/Standard_controller
# https://www.nesdev.org/wiki/Controller_reading_code
from dataclasses import dataclass


# NES Controller hardware returns bits in this order,
# First read A, second B, etc:


BUTTON_A =      1 << 0
BUTTON_B =      1 << 1
BUTTON_SELECT = 1 << 2
BUTTON_START =  1 << 3
BUTTON_UP =     1 << 4
BUTTON_DOWN =   1 << 5
BUTTON_LEFT =   1 << 6
BUTTON_RIGHT =  1 << 7

@dataclass
class Controller:
    a: bool = False
    b: bool = False
    select: bool = False
    start: bool = False
    up: bool = False
    down: bool = False
    left: bool = False
    right: bool = False

    strobe: bool = False
    captured_buttons: int = 0
    read_index: int = 0

    def capture_buttons(self) -> None:
        value = 0

        if self.a:
            value |= BUTTON_A
        if self.b:
            value |= BUTTON_B
        if self.select:
            value |= BUTTON_SELECT
        if self.start:
            value |= BUTTON_START
        if self.up:
            value |= BUTTON_UP
        if self.down:
            value |= BUTTON_DOWN
        if self.left:
            value |= BUTTON_LEFT
        if self.right:
            value |= BUTTON_RIGHT

        self.captured_buttons = value
        self.read_index = 0

    def write_strobe(self, value: int) -> None:
        """
        strobe high, keep capturing current button state
        strobe low, serial reads advance
        """
        self.strobe = (value & 1) == 1 # True or False
        
        if self.strobe:
            self.capture_buttons()


    def read_bit(self) -> int:
        """
        read order: A, B, Select, Start, Up, Down, Left, Right
        after 8 read: return 1
        """
        # Is strobe bit set? then controller should be reloaded
        if self.strobe:
            self.capture_buttons()
        # Do we already read all buttons? Then return 1
        if self.read_index >= 8:
            return 1

        bit = (self.captured_buttons >> self.read_index) & 1
        self.read_index += 1
        return bit
