from typing import Any, Literal, Optional, overload, Generator


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


class Grid:
    """General class for storing a grid of data"""

    def __init__(self, data: list, directions=Direction) -> None:
        """Initialize grid with given data

        Data is copied to avoid modifying and mutability issues
        """
        self._N = len(data)
        self._M = len(data[0])
        self.data: list[list[str]] = [
            [data[i][j] for j in range(self._M)] for i in range(self._N)
        ]
        self.neighborhood = GridNeighborhood((self._N, self._M))
        self.directions = directions
        self._updated = False
        self._items_counts: Optional[dict[str, int]] = None
        self._hash: Optional[int] = None

    @property
    def updated(self):
        return self._updated

    @property
    def N(self):
        return self._N

    @property
    def M(self):
        return self._M

    @property
    def items(self):
        """Lazy evaluated set of items in the grid"""
        if self._items_counts is None or self._updated:
            self._update_counts()
        return set(self._items_counts.keys())  # type: ignore

    @property
    def item_counts(self) -> dict[str, int]:
        """Lazy evaluated dict of item counts in the grid"""
        if self._items_counts is None or self._updated:
            self._update_counts()
        return self._items_counts  # type: ignore

    def col(self, j: int) -> list[str]:
        """Get the jth column of the grid"""
        return [self.data[i][j] for i in range(self._N)]

    def row(self, i: int) -> list[str]:
        """Get the ith row of the grid"""
        return self.data[i]

    def set_row(self, i: int, row: list[str]):
        """Set the ith row of the grid"""
        if len(row) != self._M:
            raise ValueError("Invalid length")
        self._updated = True
        self.data[i] = row

    def set_col(self, j: int, col: list[str]):
        """Set the jth column of the grid"""
        if len(col) != self._N:
            raise ValueError("Invalid length")
        self._updated = True
        for i in range(self._N):
            self.data[i][j] = col[i]

    def _update_counts(self):
        self._updated = False
        self._items_counts = {}
        for item in self.to_iter():
            self._items_counts[item] = self._items_counts.get(item, 0) + 1

    def __str__(self):
        return "\n".join("".join(row) for row in self.data)

    @overload
    def __getitem__(self, key: tuple[int, int]) -> str:
        ...

    @overload
    def __getitem__(self, key: int) -> list[str]:
        ...

    def __getitem__(self, key: tuple[int, int] | int):
        if isinstance(key, int):
            return self.data[key]
        return self.data[key[0]][key[1]]

    @overload
    def __setitem__(self, key: tuple[int, int], value: str):
        ...

    @overload
    def __setitem__(self, key: int, value: list[str]):
        ...

    def __setitem__(self, key: tuple[int, int] | int, value):
        self._updated = True
        if isinstance(key, int):
            if len(value) != self._M:
                raise ValueError("Invalid length")
            self.data[key] = [v for v in value]
            return
        self.data[key[0]][key[1]] = value

    @overload
    def to_iter(
        self, column_major: bool = False, indices: Literal[False] = False
    ) -> Generator[str, Any, None]:
        ...

    @overload
    def to_iter(
        self, column_major: bool = False, indices: Literal[True] = True
    ) -> Generator[tuple[tuple[int, int], str], Any, None]:
        ...

    def to_iter(self, column_major=False, indices=False):
        """Iterate over the grid, defaulting to row-major order"""
        if column_major:
            for j in range(self._M):
                for i in range(self._N):
                    if indices:
                        yield (i, j), self.data[i][j]
                    else:
                        yield self.data[i][j]
        else:
            for i in range(self._N):
                for j in range(self._M):
                    if indices:
                        yield (i, j), self.data[i][j]
                    else:
                        yield self.data[i][j]

    def iter_rows(self):
        """Iterate over the rows of the grid"""
        for row in self.data:
            yield row

    def iter_cols(self):
        """Iterate over the columns of the grid"""
        for j in range(self._M):
            yield [self.data[i][j] for i in range(self._N)]

    def neighbors(self, pos: tuple[int, int], diagonals=False) -> list[tuple[int, int]]:
        return self.neighborhood.get_neighbors(pos, diagonals)

    def block_neighbors(
        self, pos1: tuple[int, int], pos2: tuple[int, int], diagonals=False
    ) -> list[tuple[int, int]]:
        return self.neighborhood.get_block_neighbors(pos1, pos2, diagonals)

    def is_valid_pos(self, pos: tuple[int, int]) -> bool:
        i, j = pos
        return 0 <= i < self._N and 0 <= j < self._M

    def get_direction(self, src: tuple[int, int], dst: tuple[int, int]) -> str:
        return self.directions.get_from(src, dst)

    def move_point(self, pos: tuple[int, int], direction: str) -> tuple[int, int]:
        """Move the point in the given direction, if possible. Otherwise, stay in place."""
        new_point = self.directions.move(pos, direction)
        if self.is_valid_pos(new_point):
            return new_point
        return pos

    @property
    def hash(self):
        if self._hash is None or self._updated:
            self._hash = self._compute_hash()
        return self._hash

    def _compute_hash(self):
        return hash(tuple(tuple(row) for row in self.data))

    def __hash__(self):
        return self.hash


def manhattan_distance(pos1: tuple[int, int], pos2: tuple[int, int]) -> int:
    """Manhattan distance between two points"""
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])
