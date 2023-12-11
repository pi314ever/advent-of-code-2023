from aocd import get_data

import utils
from utils import Grid

DAY = 11
GALAXY = "#"
SPACE = "."


def main():
    data = get_data(day=DAY, year=utils.YEAR).splitlines()
    grid = Grid(data)
    assert part_1(grid) == 9627977
    assert part_2(grid) == 644248339497


def part_1(grid: Grid):
    empty_rows, empty_cols = get_empty_rows_cols(grid)
    galaxies = [pos for pos, _ in grid.to_iter(indices=True) if grid[pos] == GALAXY]
    galaxies = [expand_point(g, empty_rows, empty_cols) for g in galaxies]
    total = 0
    for i, g1 in enumerate(galaxies):
        for g2 in galaxies[i + 1 :]:
            total += utils.manhattan_distance(g1, g2)
    print("Sum of distances, expand by 1: ", total)
    return total


def part_2(grid: Grid):
    empty_rows, empty_cols = get_empty_rows_cols(grid)
    galaxies = [pos for pos, _ in grid.to_iter(indices=True) if grid[pos] == GALAXY]
    galaxies = [expand_point(g, empty_rows, empty_cols, 999999) for g in galaxies]
    total = 0
    for i, g1 in enumerate(galaxies):
        for g2 in galaxies[i + 1 :]:
            total += utils.manhattan_distance(g1, g2)
    print("Sum of distances, expand by 999999: ", total)
    return total


def expand_point(pos, empty_rows, empty_cols, extra_spaces=1):
    """Expand point to account for empty rows/cols"""
    i, j = pos
    for row in empty_rows:
        if row < pos[0]:
            i += extra_spaces
        else:
            break
    for col in empty_cols:
        if col < pos[1]:
            j += extra_spaces
        else:
            break
    return (i, j)


def get_empty_rows_cols(grid: Grid):
    # Find positions of empty rows and cols
    empty_rows = []
    empty_cols = []
    for i, row in enumerate(grid.iter_rows()):
        if not any(c == GALAXY for c in row):
            empty_rows.append(i)
    for j, col in enumerate(grid.iter_cols()):
        if not any(c == GALAXY for c in col):
            empty_cols.append(j)
    return empty_rows, empty_cols


if __name__ == "__main__":
    main()
