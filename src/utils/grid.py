from typing import Any, Literal, Optional, overload, Generator

from .typing import POS_TYPE


class GridNeighborhood:
    def __init__(self, dimensions: POS_TYPE) -> None:
        self.N, self.M = dimensions

    def get_neighbors(
        self, pos: POS_TYPE, diagonals=False, loop=False
    ) -> list[POS_TYPE]:
        i, j = pos
        neighbors = []
        if i > 0:
            neighbors.append((i - 1, j))
        elif i == 0 and loop:
            neighbors.append((self.N - 1, j))
        if i < self.N - 1:
            neighbors.append((i + 1, j))
        elif i == self.N - 1 and loop:
            neighbors.append((0, j))
        if j > 0:
            neighbors.append((i, j - 1))
        elif j == 0 and loop:
            neighbors.append((i, self.M - 1))
        if j < self.M - 1:
            neighbors.append((i, j + 1))
        elif j == self.M - 1 and loop:
            neighbors.append((i, 0))
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
        self, pos1: POS_TYPE, pos2: POS_TYPE, diagonals=False
    ) -> list[POS_TYPE]:
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
    NORTH_EAST = "NE"
    NORTH_WEST = "NW"
    SOUTH_EAST = "SE"
    SOUTH_WEST = "SW"

    ALL_COORDINATES = {
        NORTH: (-1, 0),
        SOUTH: (1, 0),
        EAST: (0, 1),
        WEST: (0, -1),
        NORTH_EAST: (-1, 1),
        NORTH_WEST: (-1, -1),
        SOUTH_EAST: (1, 1),
        SOUTH_WEST: (1, -1),
    }
    DIAGONALS = set([NORTH_EAST, NORTH_WEST, SOUTH_EAST, SOUTH_WEST])

    @staticmethod
    def get_from(src: POS_TYPE, dst: POS_TYPE, diagonal=False) -> str:
        """Get the direction from src to dst"""
        i_src, j_src = src
        i_dst, j_dst = dst
        for k, v in Direction.ALL_COORDINATES.items():
            i, j = v
            if i_dst == i_src + i and j_dst == j_src + j:
                return k
        raise ValueError("Invalid src and dst positions")

    @staticmethod
    def move(pos: POS_TYPE, direction: str, distance: int = 1) -> POS_TYPE:
        """Move the position in the given direction"""
        if direction not in Direction.ALL_COORDINATES:
            raise ValueError(
                f"Invalid direction {direction}. Valid directions: {Direction.list_names()}"
            )
        i, j = pos
        i_delta, j_delta = Direction.ALL_COORDINATES[direction]

        return (i + i_delta * distance, j + j_delta * distance)

    @staticmethod
    def list_names(diagonals=False) -> list[str]:
        if diagonals:
            return list(Direction.ALL_COORDINATES.keys())
        return list(
            k for k in Direction.ALL_COORDINATES.keys() if k not in Direction.DIAGONALS
        )

    @staticmethod
    def list_deltas(diagonals=False) -> list[POS_TYPE]:
        if diagonals:
            return list(Direction.ALL_COORDINATES.values())
        return list(
            v
            for k, v in Direction.ALL_COORDINATES.items()
            if k not in Direction.DIAGONALS
        )

    @staticmethod
    def opposite(direction: str) -> str:
        if direction == Direction.NORTH:
            return Direction.SOUTH
        if direction == Direction.SOUTH:
            return Direction.NORTH
        if direction == Direction.EAST:
            return Direction.WEST
        if direction == Direction.WEST:
            return Direction.EAST
        if direction == Direction.NORTH_EAST:
            return Direction.SOUTH_WEST
        if direction == Direction.SOUTH_WEST:
            return Direction.NORTH_EAST
        if direction == Direction.NORTH_WEST:
            return Direction.SOUTH_EAST
        if direction == Direction.SOUTH_EAST:
            return Direction.NORTH_WEST
        raise ValueError("Invalid direction")

    @staticmethod
    def rotate(direction: str, clockwise: bool = True) -> str:
        if clockwise:
            if direction == Direction.NORTH:
                return Direction.EAST
            if direction == Direction.SOUTH:
                return Direction.WEST
            if direction == Direction.EAST:
                return Direction.SOUTH
            if direction == Direction.WEST:
                return Direction.NORTH
        else:
            if direction == Direction.NORTH:
                return Direction.WEST
            if direction == Direction.SOUTH:
                return Direction.EAST
            if direction == Direction.EAST:
                return Direction.NORTH
            if direction == Direction.WEST:
                return Direction.SOUTH
        raise ValueError("Invalid direction")


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
        self._neighborhood = GridNeighborhood((self._N, self._M))
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

    @property
    def bottom_right(self) -> POS_TYPE:
        return self.N - 1, self.M - 1

    @property
    def corners(self) -> list[POS_TYPE]:
        return [(0, 0), (0, self.M - 1), (self.N - 1, 0), (self.N - 1, self.M - 1)]

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
        for item in self.iter():
            self._items_counts[item] = self._items_counts.get(item, 0) + 1

    def __str__(self):
        return "\n".join("".join(row) for row in self.data)

    @overload
    def __getitem__(self, key: POS_TYPE) -> str:
        ...

    @overload
    def __getitem__(self, key: int) -> list[str]:
        ...

    def __getitem__(self, key: POS_TYPE | int):
        if isinstance(key, int):
            return self.data[key]
        return self.data[key[0]][key[1]]

    @overload
    def __setitem__(self, key: POS_TYPE, value: str):
        ...

    @overload
    def __setitem__(self, key: int, value: list[str]):
        ...

    def __setitem__(self, key: POS_TYPE | int, value):
        self._updated = True
        if isinstance(key, int):
            if len(value) != self._M:
                raise ValueError("Invalid length")
            self.data[key] = [v for v in value]
            return
        self.data[key[0]][key[1]] = value

    @overload
    def iter(
        self, column_major: bool = False, indices: Literal[False] = False
    ) -> Generator[str, Any, None]:
        ...

    @overload
    def iter(
        self, column_major: bool = False, indices: Literal[True] = True
    ) -> Generator[tuple[POS_TYPE, str], Any, None]:
        ...

    def iter(self, column_major=False, indices=False):
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

    def linear_index(self, i: int, j: int) -> int:
        return i * self.M + j

    def iter_rows(self):
        """Iterate over the rows of the grid"""
        for row in self.data:
            yield row

    def iter_cols(self):
        """Iterate over the columns of the grid"""
        for j in range(self._M):
            yield [self.data[i][j] for i in range(self._N)]

    def neighbors(self, pos: POS_TYPE, diagonals=False) -> list[POS_TYPE]:
        return self._neighborhood.get_neighbors(pos, diagonals)

    def block_neighbors(
        self, pos1: POS_TYPE, pos2: POS_TYPE, diagonals=False
    ) -> list[POS_TYPE]:
        return self._neighborhood.get_block_neighbors(pos1, pos2, diagonals)

    def is_valid_pos(self, pos: POS_TYPE) -> bool:
        i, j = pos
        return 0 <= i < self._N and 0 <= j < self._M

    def get_direction(self, src: POS_TYPE, dst: POS_TYPE) -> str:
        return self.directions.get_from(src, dst)

    def move_point(self, pos: POS_TYPE, direction: str, distance: int = 1) -> POS_TYPE:
        """Move the point in the given direction, if possible. Otherwise, stay in place."""
        new_point = self.directions.move(pos, direction, distance)
        if self.is_valid_pos(new_point):
            return new_point
        raise ValueError(
            f"Invalid move: {pos} -- {direction}, {distance} --> {new_point}"
        )

    @property
    def hash(self):
        if self._hash is None or self._updated:
            self._hash = self._compute_hash()
        return self._hash

    def _compute_hash(self):
        return hash(tuple(tuple(row) for row in self.data))

    def __hash__(self):
        return self.hash

    def transpose(self):
        empty_grid = Grid([["" for _ in range(self.N)] for _ in range(self.M)])
        for i in range(self.N):
            for j in range(self.M):
                empty_grid[j, i] = self[i, j]
        return empty_grid

    def replace(self, old: str, new: str):
        self._updated = True
        for i in range(self.N):
            for j in range(self.M):
                if self[i, j] == old:
                    self[i, j] = new

    def find(self, item: str):
        for i in range(self.N):
            for j in range(self.M):
                if self[i, j] == item:
                    return i, j
        raise ValueError(f"Item {item} not found in grid")

    def find_all(self, item: str):
        for i in range(self.N):
            for j in range(self.M):
                if self[i, j] == item:
                    yield i, j

    def shortest_path(
        self,
        src: POS_TYPE,
        dst: POS_TYPE,
        walkable: Optional[set] = None,
        not_walkable: Optional[set] = None,
    ):
        # TODO: Implement shortest path algorithm
        pass
