from aocd import get_data

import utils

DAY = 13


def main():
    data = get_data(day=DAY, year=utils.YEAR).splitlines()
    grids = parse(data)
    test_grids = parse(TEST_A.splitlines())
    assert part_1(test_grids) == 405
    # part_1(parse(TEST_B.splitlines()))
    part_1(grids)
    assert part_2(test_grids) == 400
    part_2(parse(TEST_B.splitlines()))
    part_2(grids)


def part_1(grids):
    total = 0
    for grid in grids:
        num_left = num_cols_left(grid)
        num_above = num_rows_above(grid)
        if num_left == 0 and num_above == 0:
            print(grid, num_left, num_above)
        total += num_left
        total += 100 * num_above
    print(total)
    return total


def part_2(grids):
    total = 0
    for grid in grids:
        prev_num_left = num_cols_left(grid)
        prev_num_above = num_rows_above(grid)
        total += new_summary(grid, prev_num_left, prev_num_above)
        # all_num_left = all_num_cols_left(grid)
        # all_num_above = all_num_rows_above(grid)
        # all_num_left = [x for x in all_num_left if x != prev_num_left]
        # all_num_above = [x for x in all_num_above if x != prev_num_above]
        # print(all_num_left, all_num_above)
        # if all_num_left:
        #     total += all_num_left[0]
        # if all_num_above:
        #     total += 100 * all_num_above[0]
    print(total)
    return total


def new_summary(grid: utils.Grid, num_left, num_above):
    # Brute force
    for i in range(grid.N):
        for j in range(grid.M):
            grid[i][j] = "." if grid[i][j] == "#" else "#"
            new_num_left = all_num_cols_left(grid)
            new_num_above = all_num_rows_above(grid)
            new_num_left = [x for x in new_num_left if x != num_left]
            new_num_above = [x for x in new_num_above if x != num_above]
            if new_num_left:
                print(
                    "Fixing",
                    i,
                    j,
                    grid[i][j],
                    new_num_left,
                    new_num_above,
                    "<=",
                    num_left,
                    num_above,
                )
                return new_num_left[0]
            if new_num_above:
                print(
                    "Fixing",
                    i,
                    j,
                    grid[i][j],
                    new_num_left,
                    new_num_above,
                    "<=",
                    num_left,
                    num_above,
                )
                return 100 * new_num_above[0]
            grid[i][j] = "." if grid[i][j] == "#" else "#"
    print(grid)
    raise ValueError("No fix found")


def num_cols_left(grid: utils.Grid):
    # Find reflection axis
    # Forward loop
    l, r = 0, grid.M - 1
    while l < r:
        if grid.col(l) != grid.col(r) and r != grid.M - 1:
            r = grid.M - 1
        elif grid.col(l) != grid.col(r):
            l += 1
        else:
            l += 1
            r -= 1
    if l != r and grid.col(l) == grid.col(r):
        return l
    # Backward loop
    l, r = 0, grid.M - 1
    while l < r:
        if grid.col(l) != grid.col(r) and l != 0:
            l = 0
        elif grid.col(l) != grid.col(r):
            r -= 1
        else:
            l += 1
            r -= 1
    if l != r and grid.col(l) == grid.col(r):
        return l
    return 0


def all_num_cols_left(grid: utils.Grid):
    out = []
    # Forward loop
    l, r = 0, grid.M - 1
    while l < r:
        if grid.col(l) != grid.col(r) and r != grid.M - 1:
            r = grid.M - 1
        elif grid.col(l) != grid.col(r):
            l += 1
        else:
            l += 1
            r -= 1
    if l != r and grid.col(l) == grid.col(r):
        out.append(l)
    # Backward loop
    l, r = 0, grid.M - 1
    while l < r:
        if grid.col(l) != grid.col(r) and l != 0:
            l = 0
        elif grid.col(l) != grid.col(r):
            r -= 1
        else:
            l += 1
            r -= 1
    if l != r and grid.col(l) == grid.col(r):
        out.append(l)
    return out


def all_num_rows_above(grid: utils.Grid):
    out = []
    # Forward loop
    l, r = 0, grid.N - 1
    while l < r:
        if grid.row(l) != grid.row(r) and r != grid.N - 1:
            r = grid.N - 1
        elif grid.row(l) != grid.row(r):
            l += 1
        else:
            l += 1
            r -= 1
    if l != r and grid.row(l) == grid.row(r):
        out.append(l)
    # Backward loop
    l, r = 0, grid.N - 1
    while l < r:
        if grid.row(l) != grid.row(r) and l != 0:
            l = 0
        elif grid.row(l) != grid.row(r):
            r -= 1
        else:
            l += 1
            r -= 1
    if l != r and grid.row(l) == grid.row(r):
        out.append(l)
    return out


def num_rows_above(grid: utils.Grid):
    # Find reflection axis
    # Forward loop
    l, r = 0, grid.N - 1
    while l < r:
        if grid.row(l) != grid.row(r) and r != grid.N - 1:
            r = grid.N - 1
        elif grid.row(l) != grid.row(r):
            l += 1
        else:
            l += 1
            r -= 1
    if l != r and grid.row(l) == grid.row(r):
        return l
    # Backward loop
    l, r = 0, grid.N - 1
    while l < r:
        if grid.row(l) != grid.row(r) and l != 0:
            l = 0
        elif grid.row(l) != grid.row(r):
            r -= 1
        else:
            l += 1
            r -= 1
    if l != r and grid.row(l) == grid.row(r):
        return l
    return 0


def parse(data):
    tmp = []
    grids = []
    for line in data:
        line.strip()
        if line == "":
            grids.append(utils.Grid(tmp))
            tmp = []
            continue
        tmp.append(line)
    if tmp:
        grids.append(utils.Grid(tmp))
    return grids


TEST_A = """#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#
"""

TEST_B = """#.##..#.##.#..#
.#...####.##.#.
###........#..#
####.#...#.....
.####.#.....##.
.####.#.#...##.
####.#...#.....
###........#..#
.#...####.##.#.
#.##..#.##.#..#
##....##.#...##
.##..###.#...#.
..##..#.###.###
..#.#.##....#.#
..#.#.##....#.#

#.##..#.##.#..#
.#...####.##.#.
###........#..#
####.#...#.....
.####.#.....##.
.####.#.....##.
####.#...#.....
###........#..#
.#...####.##.#.
#.##..#.##.#..#
##....##.#...##
.##..###.#...#.
..##..#.###.###
..#.#.##....#.#
..#.#.##.#..#.#
"""


if __name__ == "__main__":
    main()
