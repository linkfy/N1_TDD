# https://www.nesdev.org/wiki/PPU_pattern_tables
def decode_chr_tile(tile_bytes: bytes) -> list[list[int]]:
    """A tile is 16 bytes Bit 0 in first plane, Bit 1 in second plane
    8 Rows for the first plane
    8 Rows for the second plane
    Each pixel becomes a number 0, 1, 2 or 3 -> 00, 01, 10, 11 (binary)
    
    Output: 
    8 rows x 8 columns
    [
        [0,1,2,3,0,1,2,3],
        ...
    ]
    Invariants: 
        len tile_bytes -> 16
        len result -> 8
        len result[row] -> 8
        pixel value -> 0 | 1 | 2 | 3
    """
    ROW_SIZE = 8
    COL_SIZE = 8
    if len(tile_bytes) != 16:
        raise ValueError("To decode CHR tile, tile must be 16 bytes")
    
    rows = []

    for row in range(ROW_SIZE):
        low_byte = tile_bytes[row]
        high_byte = tile_bytes[row+8]
        columns = []
        for col in range(COL_SIZE):
            bit_position = 7 - col
            low = (low_byte >> bit_position) & 1 # Convert to 1 bit | Example 0b1000_000 -> 0b1
            high = (high_byte >> bit_position) & 1 # Convert to 1 bit
            pixel = (high << 1) | low
            columns.append(pixel)

        rows.append(columns)
    return rows
            

        

    

    
