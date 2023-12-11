from aocd import get_data

import utils
from utils import Grid

DAY = 11
GALAXY = "#"
SPACE = "."


def main():
    data = get_data(day=DAY, year=utils.YEAR).splitlines()
    grid = Grid(data)
    expanded_grid = expand(grid)
    part_1(expanded_grid)
    part_2(grid)


def part_1(grid: Grid):
    galaxies = [pos for pos, _ in grid.to_iter(indices=True) if grid[pos] == GALAXY]
    total = 0
    for i, g1 in enumerate(galaxies):
        for g2 in galaxies[i + 1 :]:
            total += utils.manhattan_distance(g1, g2)
    print(total)
    return total


def part_2(grid: Grid):
    # Find positions of empty rows and cols
    empty_rows = []
    empty_cols = []
    for i, row in enumerate(grid.iter_rows()):
        if not any(c == GALAXY for c in row):
            empty_rows.append(i)
    for j, col in enumerate(grid.iter_cols()):
        if not any(c == GALAXY for c in col):
            empty_cols.append(j)
    galaxies = [pos for pos, _ in grid.to_iter(indices=True) if grid[pos] == GALAXY]
    galaxies = [expand_point(g, empty_rows, empty_cols, 999999) for g in galaxies]
    total = 0
    for i, g1 in enumerate(galaxies):
        for g2 in galaxies[i + 1 :]:
            total += utils.manhattan_distance(g1, g2)
    print(total)
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


def expand(grid: Grid):
    """Expand grid for every row/col of empty space"""
    new_grid = []
    for row in grid.iter_rows():
        for c in row:
            if c == GALAXY:
                new_grid.append(row)
                break
        else:
            new_grid.append(row)
            new_grid.append(row)
    grid = Grid(new_grid)
    new_grid = []
    for col in grid.iter_cols():
        for c in col:
            if c == GALAXY:
                new_grid.append(col)
                break
        else:
            new_grid.append(col)
            new_grid.append(col)
    grid = Grid(new_grid)
    return Grid([*list(grid.iter_cols())])


if __name__ == "__main__":
    main()
