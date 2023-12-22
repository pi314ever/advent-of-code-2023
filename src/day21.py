from aocd import get_data
from collections import deque
from tqdm import tqdm

import utils
from utils import Grid, InfiniteGrid, Direction

DAY = 21

START = "S"
GARDEN_PLOT = "."
ROCK = "#"


def main():
    data = get_data(day=DAY, year=utils.YEAR).splitlines()
    test_data = TEST.splitlines()
    test_grid = Grid(test_data)
    grid = Grid(data)
    part_1(grid)
    # part_2(test_grid, 5000)
    part_2(grid)
    # quadratic(grid)


def part_1(grid: Grid):
    total = bfs_search(grid)
    print(total)
    return total


def part_2(grid: Grid, n_steps=26501365):
    infinite_grid = InfiniteGrid.from_grid(grid)

    # Split n_steps into remainder and number of chunks
    tiles, remainder = divmod(n_steps, infinite_grid.N)
    points = []
    # Iterate three times
    steps = [remainder + infinite_grid.N * i for i in range(3)]
    print(steps)
    for s in steps:
        points.append(bfs_search(infinite_grid, s))
        # print("point", len(points), points[-1], "after", s, "steps")

    def f(n):
        y0 = points[0]
        y1 = points[1]
        y2 = points[2]
        a = (y2 + y0 - 2 * y1) / 2
        b = y1 - y0 - a
        c = y0
        return a * n**2 + b * n + c

    assert all(
        f(i) == p for i, p in enumerate(points)
    ), "Error in quadratic extrapolation"

    ans = int(f(n_steps // infinite_grid.N))
    print(ans)
    return ans


def bfs_search(grid: Grid, depth=64):
    start = grid.find(START)
    q = deque()
    q.append((start, 0))
    seen = set()
    total = 0
    step = 0
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    with tqdm(total=depth, leave=False) as pbar:
        while q:
            pos, dist = q.popleft()
            if dist > depth:
                break
            if pos in seen:
                continue
            seen.add(pos)
            if step < dist:
                pbar.update(dist - step)
                # pbar.display(f"len(q) = {len(q)}")
                step = dist
            if dist % 2 == depth % 2:
                total += 1
            if dist < depth:
                for dx, dy in directions:
                    neighbor = (pos[0] + dx, pos[1] + dy)
                    if grid[neighbor] != ROCK:
                        q.append((neighbor, dist + 1))
    return total


def part_2_direct(grid: Grid, n_steps=26501365):
    # TODO: Pre-compute the distances from 9 key points to all other points.
    # Data is structured as:
    #  grid: (n x m)
    #        m
    #   _____|_____
    #  | m/2 | m/2 |
    #  A.....B.....C   |
    #  .     .     .   |-> n/2
    #  .     .     .   |
    #  D.....S.....E   ---------->  n
    #  .     .     .   |
    #  .     .     .   |-> n/2
    #  F.....G.....H   |
    # Where S is the start and the letters are external entrances.
    # The shortest distance from S to some point (P) n_steps distance away from S to the right is:
    # w_2 + m * ((n_steps - w_2) // m) + distance[D][local[P]] == n_steps
    #
    # This solution requires n == m both odd, n_steps % n == n // 2, and S to be in the center.
    #

    infinite_grid = InfiniteGrid.from_grid(grid)
    start = infinite_grid.find(START)

    assert grid.N == grid.M, "Grid must be square"
    assert start == (grid.N // 2, grid.M // 2), "Start must be in the center"
    assert grid.N % 2 == 1, "Grid must have odd width"

    # Split n_steps into remainder and number of chunks
    tiles, remainder = divmod(n_steps, infinite_grid.N)

    # Precompute distances from key points
    key_points = grid.corners + [
        (0, start[1]),
        (infinite_grid.N - 1, start[1]),
        (start[0], 0),
        (start[0], infinite_grid.M - 1),
    ]
    search_distances = [65] * 4 + [131] * 4


TEST = """...........
.....###.#.
.###.##..#.
..#.#...#..
....#.#....
.##..S####.
.##..#...#.
.......##..
.##.#.####.
.##..##.##.
..........."""

if __name__ == "__main__":
    main()
