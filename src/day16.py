from aocd import get_data
from timeit import default_timer as timer

import utils
from utils import Grid, Direction

DAY = 16

EMPTY = "."
MIRRORS = ["/", "\\"]
SPLITTERS = ["|", "-"]


def main():
    data = get_data(day=DAY, year=utils.YEAR).splitlines()
    # part_1(TEST_INPUT.splitlines())
    assert part_1(data) == 6361
    # part_2(TEST_INPUT.splitlines())
    timer_start = timer()
    assert part_2(data) == 6701
    timer_end = timer()
    print(f"Completed part 2 in {timer_end - timer_start} seconds")


def part_1(data):
    grid = BeamGrid(data)
    grid.simulate()
    num_energized = grid.get_num_energized()
    print(num_energized)
    return num_energized


def part_2(data):
    grid = BeamGrid(data)
    configurations = []
    # Top row
    for j in range(grid.M):
        grid.reset_energized()
        grid.simulate((0, j), Direction.SOUTH)
        configurations.append(grid.get_num_energized())
    # Right column
    for i in range(grid.N):
        grid.reset_energized()
        grid.simulate((i, grid.M - 1), Direction.WEST)
        configurations.append(grid.get_num_energized())
    # Bottom row
    for j in range(grid.M):
        grid.reset_energized()
        grid.simulate((grid.N - 1, j), Direction.NORTH)
        configurations.append(grid.get_num_energized())
    # Left column
    for i in range(grid.N):
        grid.reset_energized()
        grid.simulate((i, 0), Direction.EAST)
        configurations.append(grid.get_num_energized())
    max_energy = max(configurations)
    print(max_energy)
    return max_energy


class BeamGrid(Grid):
    def __init__(self, data: list) -> None:
        super().__init__(data)
        self.energized = [[False for _ in range(self.M)] for _ in range(self.N)]

    def reset_energized(self):
        self.energized = [[False for _ in range(self.M)] for _ in range(self.N)]

    def simulate(self, start=(0, 0), direction=Direction.EAST):
        # DFS on the beams, keeping track of all seen beam directions
        beam: list[tuple[tuple[int, int], str]] = [(start, direction)]
        seen = set()
        while beam:
            pos, direction = beam.pop()
            if (pos, direction) in seen:
                continue
            seen.add((pos, direction))
            self.energized[pos[0]][pos[1]] = True
            # Check what to do next
            if self[pos] == EMPTY:
                new_pos = self.move_point(pos, direction)
                new_direction = direction
            elif self[pos] in MIRRORS:
                new_direction = reflect_mirror(direction, self[pos])
                new_pos = self.move_point(pos, new_direction)
            elif self[pos] in SPLITTERS:
                new_direction = split_beam(direction, self[pos])
                for d in new_direction:
                    new_pos = self.move_point(pos, d)
                    if pos != new_pos:
                        beam.append((new_pos, d))
                continue
            else:
                raise ValueError("Invalid character")

            if pos != new_pos:
                beam.append((new_pos, new_direction))

    def get_num_energized(self):
        return sum(sum(row) for row in self.energized)


MIRROR_MAP = {
    "/": {
        Direction.NORTH: Direction.EAST,
        Direction.EAST: Direction.NORTH,
        Direction.SOUTH: Direction.WEST,
        Direction.WEST: Direction.SOUTH,
    },
    "\\": {
        Direction.NORTH: Direction.WEST,
        Direction.WEST: Direction.NORTH,
        Direction.SOUTH: Direction.EAST,
        Direction.EAST: Direction.SOUTH,
    },
}


def reflect_mirror(direction: str, mirror: str) -> str:
    """Reflect the direction off the mirror"""
    if mirror not in MIRRORS:
        raise ValueError("Invalid mirror")
    return MIRROR_MAP[mirror][direction]


SPLIT_MAP = {
    "|": {
        Direction.NORTH: [Direction.NORTH],
        Direction.SOUTH: [Direction.SOUTH],
        Direction.EAST: [Direction.NORTH, Direction.SOUTH],
        Direction.WEST: [Direction.SOUTH, Direction.NORTH],
    },
    "-": {
        Direction.NORTH: [Direction.EAST, Direction.WEST],
        Direction.SOUTH: [Direction.EAST, Direction.WEST],
        Direction.EAST: [Direction.EAST],
        Direction.WEST: [Direction.WEST],
    },
}


def split_beam(direction: str, split: str) -> list[str]:
    """Split the beam into two"""
    if split not in SPLITTERS:
        raise ValueError("Invalid splitter")
    return SPLIT_MAP[split][direction]


TEST_INPUT = r""".|...\....
|.-.\.....
.....|-...
........|.
..........
.........\
..../.\\..
.-.-/..|..
.|....-|.\
..//.|....
"""

if __name__ == "__main__":
    main()
