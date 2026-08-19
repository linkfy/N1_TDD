"""
Attribute table is a 64-byte array at the end of each nametable
Controls palette assigned to each part of the background
https://www.nesdev.org/wiki/PPU_attribute_tables
It is a 8x8 => 64 table positions
       2xx0    2xx1    2xx2    2xx3    2xx4    2xx5    2xx6    2xx7
     ,-------+-------+-------+-------+-------+-------+-------+-------.
     |   .   |   .   |   .   |   .   |   .   |   .   |   .   |   .   |
2xC0:| - + - | - + - | - + - | - + - | - + - | - + - | - + - | - + - |
     |   .   |   .   |   .   |   .   |   .   |   .   |   .   |   .   |
     +-------+-------+-------+-------+-------+-------+-------+-------+
     |   .   |   .   |   .   |   .   |   .   |   .   |   .   |   .   |
2xC8:| - + - | - + - | - + - | - + - | - + - | - + - | - + - | - + - |
     |   .   |   .   |   .   |   .   |   .   |   .   |   .   |   .   |
     +-------+-------+-------+-------+-------+-------+-------+-------+
     ....
     ....
2xF8:|

Each byte controls 4x4 tile parts (32x32 pixels)

"""

TABLE_SIZE = 64
BYTES_PER_ROW = 8

def get_attribute_palette_id(
        attribute_table: bytes,
        tile_x: int,
        tile_y: int,
) -> int:
    if len(attribute_table) != TABLE_SIZE:
        raise ValueError("Attribute table must be 64 bytes")

    attribute_x = tile_x // 4 # Each 4x4 tiles is controlled by 1 byte
    attribute_y = tile_y // 4 # of Attribute table

    attribute_index = attribute_y * BYTES_PER_ROW + attribute_x
    attribute_byte = attribute_table[attribute_index]
    # 4x4 tiles per attribute byte
    # top-left      2x2 tiles -> bits 0-1
    # top-right     2x2 tiles -> bits 2-3
    # bottom-left   2x2 tiles -> bits 4-5
    # bottom-right  2x2 tiles -> bits 6-7
    # Calculate mod % 4 obtains -> 0, 1, 2, 3
    
    # Quadrants can have value 0 or 1, 
    # we do the mod % 4 to obtain 0, 1, 2, 3
    # We do //2 to split:
    # 0, 1 to quadrant 0 
    # 2, 3 to quadrant 1

    quadrant_x = (tile_x % 4) // 2 # assigns 0 or 1
    quadrant_y = (tile_y % 4) // 2 # assigns 0 or 1 
    """
    Detect in which location we are
    +-------+
    |   .   |
    | - + - |
    |   .   |
    +-------+
    """
    is_top_left     = (quadrant_x == 0) and (quadrant_y == 0)
    is_top_right    = (quadrant_x == 1) and (quadrant_y == 0)
    is_bottom_left  = (quadrant_x == 0) and (quadrant_y == 1)
    is_bottom_right = (quadrant_x == 1) and (quadrant_y == 1)
    """
    On each attribute byte
    7654 3210
    |||| ||++- Color bits for top left quadrant of this byte
    |||| ++--- Color bits for top right quadrant of this byte
    ||++------ Color bits for bottom left quadrant of this byte
    ++-------- Color bits for bottom right quadrant of this byte
    """
    # Return palette_id based on location
    if is_top_left:
        return attribute_byte & 0b11
    elif is_top_right:
        return (attribute_byte >> 2) & 0b11
    elif is_bottom_left:
        return (attribute_byte >> 4) & 0b11
    else: # bottom_right
        return (attribute_byte >> 6) & 0b11



