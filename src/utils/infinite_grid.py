from utils.grid import Direction
from .grid import Grid, Direction, GridNeighborhood
from .typing import POS_TYPE


class InfiniteGridNeighborhood(GridNeighborhood):
    def __init__(self) -> None:
        self.N = None
        self.M = None

    def get_neighbors(self, pos: POS_TYPE, diagonals=False) -> list[POS_TYPE]:
        return [
            (pos[0] + dx, pos[1] + dy) for dx, dy in Direction.list_deltas(diagonals)
        ]


class InfiniteGrid(Grid):
    """Infinite grid helper class"""

    def __init__(self, data: list, directions=Direction) -> None:
        super().__init__(data, directions)

    @classmethod
    def from_grid(cls, grid: Grid):
        """Create an InfiniteGrid from a Grid"""
        new_grid = cls(grid.data, grid.directions)
        return new_grid

    def is_valid_pos(self, pos: POS_TYPE) -> bool:
        """Always valid position in infinite grid"""
        return True

    def global_to_local_idx(self, pos: POS_TYPE) -> tuple[POS_TYPE, POS_TYPE]:
        """Convert global position to local position

        Returns (grid_pos, local_pos):
            grid_pos: Grid position within the infinite grid
            local_pos: Position within the grid
        """
        x, y = pos
        g_x, g_y = x // self.N, y // self.M
        l_x, l_y = x % self.N, y % self.M
        return (g_x, g_y), (l_x, l_y)

    def __getitem__(self, key: POS_TYPE):
        _, (x, y) = self.global_to_local_idx(key)
        return self.data[x][y]

    def __setitem__(self, key: POS_TYPE, value):
        _, (x, y) = self.global_to_local_idx(key)
        self.data[x][y] = value
