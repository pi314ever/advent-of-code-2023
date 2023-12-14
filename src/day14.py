from aocd import get_data
from functools import cache

import utils
from utils import Grid

DAY = 14

ROUND_ROCK = "O"
CUBE_ROCK = "#"
EMPTY = "."


def main():
    data = get_data(day=DAY, year=utils.YEAR).splitlines()
    grid = Grid(data)
    # assert part_1(Grid(TEST_DATA.splitlines())) == 136
    part_1(grid)
    # assert part_2(Grid(TEST_DATA.splitlines())) == 64
    part_2(grid)


def part_1(grid: Grid):
    tilt_north(grid)
    total_load = sum_load(grid)
    print(total_load)
    return total_load


def part_2(grid: Grid):
    num_cycles = 1000000000  # 1e9
    seen = {}
    grids = []
    prev_idx: int
    cycle_len: int
    for i in range(num_cycles):
        if grid.hash in seen:
            grid, prev_idx = seen[grid.hash]
            cycle_len = i - prev_idx
            break
        else:
            tmp = Grid(grid.data)
            cycle(grid)
            seen[tmp.hash] = grid, i
        grids.append(Grid(grid.data))
    else:
        raise RuntimeError("Did not find cycle")
    # Calculate the index of the grid after 1e9 cycles
    idx = (num_cycles - prev_idx) % cycle_len + prev_idx - 1
    grid = grids[idx]

    total_load = sum_load(grid)
    print(total_load)
    return total_load


def tilt_north(grid: Grid):
    """Mutates the grid to tilt the rocks north"""
    for j, col in enumerate(grid.iter_cols()):
        place = 0
        for i in range(len(col)):
            cell = col[i]
            if cell == EMPTY:
                continue
            if cell == ROUND_ROCK:
                grid[i, j] = EMPTY
                grid[place, j] = ROUND_ROCK
                col[i] = EMPTY
                col[place] = ROUND_ROCK
                place += 1
            elif cell == CUBE_ROCK:
                place = i + 1


def tilt_west(grid: Grid):
    """Mutates the grid to tilt the rocks west"""
    for i, row in enumerate(grid.iter_rows()):
        place = 0
        for j in range(len(row)):
            cell = row[j]
            if cell == EMPTY:
                continue
            if cell == ROUND_ROCK:
                grid[i, j] = EMPTY
                grid[i, place] = ROUND_ROCK
                row[j] = EMPTY
                row[place] = ROUND_ROCK
                place += 1
            elif cell == CUBE_ROCK:
                place = j + 1


def tilt_south(grid: Grid):
    """Mutates the grid to tilt the rocks south"""
    for j, col in enumerate(grid.iter_cols()):
        place = grid.N - 1
        for i in range(grid.N - 1, -1, -1):
            cell = col[i]
            if cell == EMPTY:
                continue
            if cell == ROUND_ROCK:
                grid[i, j] = EMPTY
                grid[place, j] = ROUND_ROCK
                col[i] = EMPTY
                col[place] = ROUND_ROCK
                place -= 1
            elif cell == CUBE_ROCK:
                place = i - 1


def tilt_east(grid: Grid):
    """Mutates the grid to tilt the rocks east"""
    for i, row in enumerate(grid.iter_rows()):
        place = grid.M - 1
        for j in range(grid.M - 1, -1, -1):
            cell = row[j]
            if cell == EMPTY:
                continue
            if cell == ROUND_ROCK:
                grid[i, j] = EMPTY
                grid[i, place] = ROUND_ROCK
                row[j] = EMPTY
                row[place] = ROUND_ROCK
                place -= 1
            elif cell == CUBE_ROCK:
                place = j - 1


def cycle(grid: Grid):
    """Mutates the grid to cycle the rocks"""
    tilt_north(grid)
    tilt_west(grid)
    tilt_south(grid)
    tilt_east(grid)


def sum_load(grid: Grid):
    """Returns the sum of the load of the grid"""
    total = 0
    for i, row in enumerate(grid.iter_rows()):
        # print(grid.M - i, len([cell for cell in row if cell == ROUND_ROCK]))
        total += len([cell for cell in row if cell == ROUND_ROCK]) * (grid.M - i)
    return total


TEST_DATA = """O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#....
"""


if __name__ == "__main__":
    main()
