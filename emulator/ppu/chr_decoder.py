PATTERN_TABLE_SIZE = 0x1000
CHR_TILE_SIZE = 16
PATTERN_TABLE_TILE_COUNT = 256

#Each pattern table is a 128 by 128 pixel square, with 16 rows and 16 tiles
PATTERN_TABLE_TILES_PER_ROW = 16
CHR_TILE_WIDTH = 8
CHR_TILE_HEIGHT = 8
PATTERN_TABLE_DEBUG_GRID_SIZE = 128

# Type alias
PatternTile = list[list[int]]
# https://www.nesdev.org/wiki/PPU_pattern_tables
def decode_chr_tile(tile_bytes: bytes) -> PatternTile:
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
            low = (low_byte >> bit_position) & 1 # Convert to 1 bit. Example: reading bit 7 0b1000_0000 -> gives 1
            high = (high_byte >> bit_position) & 1 # Convert to 1 bit
            pixel = (high << 1) | low
            columns.append(pixel)

        rows.append(columns)
    return rows

# Type alias:
PatternTable = list[PatternTile]
def decode_pattern_table(pattern_table_bytes: bytes) -> PatternTable:
    """
    A pattern table contains 256 pattern tiles, each tile has 16 bytes
    Total pattern table size = 4096 (0x1000)
    """
    if len(pattern_table_bytes) != PATTERN_TABLE_SIZE:
        raise ValueError("Pattern table must be 4096 bytes")

    tiles = []

    for tile_index in range(PATTERN_TABLE_TILE_COUNT):
        start = tile_index * CHR_TILE_SIZE
        end = start + CHR_TILE_SIZE
        tiles.append(decode_chr_tile(pattern_table_bytes[start:end]))

    return tiles


# Type Alias:
PatternTableDebugGrid = list[list[int]]
def build_pattern_table_debug_grid(decoded_tiles: PatternTable) -> PatternTableDebugGrid:
    """Each pattern table is a 128 by 128 pixel square, with 16 rows and 16 tiles
    This debug function helps to verify correct grid construction based on pattern table
    """
    if len(decoded_tiles) != PATTERN_TABLE_TILE_COUNT:
        raise ValueError("Pattern table debug grid requires 256 decoded tiles")

    grid = [
            [0 for _ in range(PATTERN_TABLE_DEBUG_GRID_SIZE)] 
            for _ in range(PATTERN_TABLE_DEBUG_GRID_SIZE)
    ]

    for tile_index, tile in enumerate(decoded_tiles):
        tile_x = (tile_index % PATTERN_TABLE_TILES_PER_ROW) * CHR_TILE_WIDTH
        tile_y = (tile_index // PATTERN_TABLE_TILES_PER_ROW) * CHR_TILE_HEIGHT

        for row in range(CHR_TILE_HEIGHT):
            for col in range(CHR_TILE_WIDTH):
                grid[tile_y + row][tile_x + col] = tile[row][col]

    return grid
