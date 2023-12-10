from .typing import _LenSupport


class Grid:
    """General class for storing a grid of data"""

    def __init__(self, data: list[_LenSupport]) -> None:
        self.N = len(data)
        self.M = len(data[0])
        self.data = data

    def __getitem__(self, key: tuple[int, int]):
        return self.data[key[0]][key[1]]


class GridNeighborhood:
    def __init__(self, dimensions: tuple[int, int]) -> None:
        self.N, self.M = dimensions

    def get_neighbors(
        self, pos: tuple[int, int], diagonals=False
    ) -> list[tuple[int, int]]:
        i, j = pos
        neighbors = []
        if i > 0:
            neighbors.append((i - 1, j))
        if i < self.N - 1:
            neighbors.append((i + 1, j))
        if j > 0:
            neighbors.append((i, j - 1))
        if j < self.M - 1:
            neighbors.append((i, j + 1))
        if diagonals:
            if i > 0 and j > 0:
                neighbors.append((i - 1, j - 1))
            if i > 0 and j < self.M - 1:
                neighbors.append((i - 1, j + 1))
            if i < self.N - 1 and j > 0:
                neighbors.append((i + 1, j - 1))
            if i < self.N - 1 and j < self.M - 1:
                neighbors.append((i + 1, j + 1))
        return neighbors

    def get_block_neighbors(
        self, pos1: tuple[int, int], pos2: tuple[int, int], diagonals=False
    ) -> list[tuple[int, int]]:
        """Get the neighbors of the rectangle defined by pos1 and pos2"""
        neighbors = []
        i1, j1 = pos1
        i2, j2 = pos2
        i_min, i_max = min(i1, i2), max(i1, i2)
        j_min, j_max = min(j1, j2), max(j1, j2)
        # Top edge
        if i_min > 0:
            # Top left corner
            if diagonals and j_min > 0:
                neighbors.append((i_min - 1, j_min - 1))
            for j in range(j_min, j_max + 1):
                neighbors.append((i_min - 1, j))
            # Top right corner
            if diagonals and j_max < self.M - 1:
                neighbors.append((i_min - 1, j_max + 1))
        # Bottom edge
        if i_max < self.N - 1:
            # Bottom left corner
            if diagonals and j_min > 0:
                neighbors.append((i_max + 1, j_min - 1))
            for j in range(j_min, j_max + 1):
                neighbors.append((i_max + 1, j))
            # Bottom right corner
            if diagonals and j_max < self.M - 1:
                neighbors.append((i_max + 1, j_max + 1))
        # Left edge
        if j_min > 0:
            for i in range(i_min, i_max + 1):
                neighbors.append((i, j_min - 1))
        # Right edge
        if j_max < self.M - 1:
            for i in range(i_min, i_max + 1):
                neighbors.append((i, j_max + 1))
        return neighbors


class Direction:
    NORTH = "N"
    SOUTH = "S"
    EAST = "E"
    WEST = "W"

    COORDINATES = {
        NORTH: (-1, 0),
        SOUTH: (1, 0),
        EAST: (0, 1),
        WEST: (0, -1),
    }

    @staticmethod
    def get_from(src: tuple[int, int], dst: tuple[int, int]) -> str:
        """Get the direction from src to dst"""
        i_src, j_src = src
        i_dst, j_dst = dst
        for k, v in Direction.COORDINATES.items():
            i, j = v
            if i_dst == i_src + i and j_dst == j_src + j:
                return k
        raise ValueError("Invalid src and dst positions")

    @staticmethod
    def move(pos: tuple[int, int], direction: str) -> tuple[int, int]:
        """Move the position in the given direction"""
        i, j = pos
        i_delta, j_delta = Direction.COORDINATES[direction]
        return (i + i_delta, j + j_delta)
