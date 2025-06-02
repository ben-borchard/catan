# Static sizes
from typing import Final, List, Set

TOTAL_TILES: Final[int] = 19
TOTAL_CORNERS: Final[int] = 54
TOTAL_EDGES: Final[int] = 72
TOTAL_MARKERS: Final[int] = 12

# List of corners (by index) on each tile (by index)
TILE_TO_CORNERS: Final[List[List[int]]] = [
    # row 1
    [0, 1, 2, 8, 9, 10],
    [2, 3, 4, 10, 11, 12],
    [4, 5, 6, 12, 13, 14],
    # row 2
    [7, 8, 9, 17, 18, 19],
    [9, 10, 11, 19, 20, 21],
    [11, 12, 13, 21, 22, 23],
    [13, 14, 15, 23, 24, 25],
    # row 3
    [16, 17, 18, 27, 28, 29],
    [18, 19, 20, 29, 30, 31],
    [20, 21, 22, 31, 32, 33],
    [22, 23, 24, 33, 34, 35],
    [24, 25, 26, 35, 36, 37],
    # row 4
    [28, 29, 30, 38, 39, 40],
    [30, 31, 32, 40, 41, 42],
    [32, 33, 34, 42, 43, 44],
    [34, 35, 36, 44, 45, 46],
    # row 5
    [39, 40, 41, 47, 48, 49],
    [41, 42, 43, 49, 50, 51],
    [43, 44, 45, 51, 52, 53]
]

# List corners per port (port type is not implied here)
PORT_TO_CORNERS: List[List[int]] = [
    [0, 1],
    [3, 4],
    [7, 17],
    [14, 15],
    [26, 37],
    [28, 38],
    [45, 46],
    [47, 48],
    [50, 51],
]

# List of edges (by index) on each tile (by index)
TILE_TO_EDGES: List[List[int]] = [
    # row 1
    [0, 1, 6, 7, 11, 12],
    [2, 3, 7, 8, 13, 14],
    [4, 5, 8, 9, 15, 16],
    # row 2
    [10, 11, 18, 19, 24, 25],
    [12, 13, 19, 20, 26, 27],
    [14, 15, 20, 21, 28, 29],
    [16, 17, 21, 22, 30, 31],
    # row 3
    [23, 24, 33, 34, 39, 40],
    [25, 26, 34, 35, 41, 42],
    [27, 28, 35, 36, 43, 44],
    [29, 30, 36, 37, 45, 46],
    [31, 32, 37, 38, 47, 48],
    # row 4
    [40, 41, 49, 50, 54, 55],
    [42, 43, 50, 51, 56, 57],
    [44, 45, 51, 52, 58, 59],
    [46, 47, 52, 53, 60, 61],
    # row 5
    [55, 56, 62, 63, 66, 67],
    [57, 58, 63, 64, 68, 69],
    [59, 60, 64, 65, 70, 71],
]

# List of the corner indexes within `TILE_TO_CORNERS` for each edge index within `TILE_TO_EDGES`
# Used to create other static index mappings (see below)
EDGE_IDX_TO_CORNERS_IDX: Final[List[List[int]]] = [
    [0, 1],
    [1, 2],
    [0, 3],
    [2, 5],
    [3, 4],
    [4, 5]
]

# List of corners (by index) at the end of an edge (by index)
EDGES_TO_CORNERS: List[List[int]] = [None] * TOTAL_EDGES
for tile in range(TOTAL_TILES):
    # six edges per tile
    for edge_idx in range(6):
        corner_idx_one = EDGE_IDX_TO_CORNERS_IDX[edge_idx][0]
        corner_idx_two = EDGE_IDX_TO_CORNERS_IDX[edge_idx][1]
        EDGES_TO_CORNERS[TILE_TO_EDGES[tile][edge_idx]] = [TILE_TO_CORNERS[tile][corner_idx_one],
                                                           TILE_TO_CORNERS[tile][corner_idx_two]]

# List of edges (by index) for each that touch a corner (by index)
CORNERS_TO_EDGES: List[List[int]] = [[] for _ in range(TOTAL_CORNERS)]
for edge in range(TOTAL_EDGES):
    for i in range(2):
        corner = EDGES_TO_CORNERS[edge][i]
        if edge not in CORNERS_TO_EDGES[corner]:
            CORNERS_TO_EDGES[corner].append(edge)

# Set of neighbor corners (one edge apart, including current), by index, by corner (by index)
CORNER_NEIGHBORS: Final[List[Set[int]]] = [set() for _ in range(TOTAL_CORNERS)]
for corner in range(TOTAL_CORNERS):
    for edge in CORNERS_TO_EDGES[corner]:
        for neighbor_corner in EDGES_TO_CORNERS[edge]:
            CORNER_NEIGHBORS[corner].add(neighbor_corner)


def connected(edge: int, corner: int) -> bool:
    """
    returns `True` if the edge is connected to the corner, otherwise `False`
    """
    return corner in EDGES_TO_CORNERS[edge]


def common_corner(edge_one: int, edge_two: int) -> int:
    """
    returns the common corner of two edges
    """
    for i in EDGES_TO_CORNERS[edge_one]:
        for j in EDGES_TO_CORNERS[edge_two]:
            if i == j:
                return i


def next_corner(edge: int, from_edge: int) -> int:
    """
    returns the next corner to check on given edge coming from the connected edge
    """
    common = common_corner(edge, from_edge)
    return EDGES_TO_CORNERS[edge][0] if EDGES_TO_CORNERS[edge][0] != common else EDGES_TO_CORNERS[edge][1]

