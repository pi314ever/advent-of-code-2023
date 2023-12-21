from aocd import get_data
from collections import deque
import numpy as np
from scipy.sparse import csr_matrix, lil_matrix
from tqdm import tqdm

import utils
from utils import Grid, InfiniteGrid

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
    part_2(test_grid, 5000)
    # part_2(grid)


def part_1(grid: Grid):
    start = grid.find(START)
    q = deque()
    q.append((start, 0))
    seen = set()
    total = 0
    step = 0
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    with tqdm(total=64) as pbar:
        while q:
            pos, dist = q.popleft()
            if dist > 64:
                break
            if pos in seen:
                continue
            seen.add(pos)
            if step < dist:
                pbar.update(dist - step)
                # pbar.display(f"len(q) = {len(q)}")
                step = dist
            if dist % 2 == 64 % 2:
                total += 1
            if dist < 64:
                for dx, dy in directions:
                    neighbor = (pos[0] + dx, pos[1] + dy)
                    if grid[neighbor] != ROCK:
                        q.append((neighbor, dist + 1))
    print(total)
    return total


def part_2(grid: Grid, n_steps=26501365):
    # TODO: Pre-compute the distances from 9 key points to all other points.
    # Data is structured as:
    #  grid: (n x m)
    #   w_1 + w_2 = m
    #   _____|_____
    #  | w_1 | w_2 |
    #  A.....B.....C   |
    #  .     .     .   |-> l_1
    #  .     .     .   |
    #  D.....S.....E   ----------> l_1 + l_2 = n
    #  .     .     .   |
    #  .     .     .   |-> l_2
    #  F.....G.....H   |
    # Where S is the start and the letters are external entrances.
    # The shortest distance from S to some point (P) n_steps distance away from S to the right is:
    # w_2 + m * ((n_steps - w_2) // m) + distance[D][local[P]] == n_steps
    #
    ...


# def propagation_diamonds(start: tuple[int, int], n_steps):
#     "Gives yields diamond of positions reachable in n_steps"
#     x, y = start


def matrix_pow(mat, n):
    if n == 0:
        return np.identity(mat.shape[0])
    if n == 1:
        return mat
    memory = [mat]
    pow = 1
    num_powers = int(np.log(n) / np.log(2))
    for i in range(num_powers):
        print(pow)
        memory.append(memory[-1] @ memory[-1])
        pow *= 2
    # Use powers of 2 to build up to n
    result = memory[-1]
    print(n)
    n -= pow
    for i in range(num_powers - 1, -1, -1):
        print(n, 2**i)
        if n >= 2**i:
            result = result @ memory[i]
            n -= 2**i
    return result


def adj_matrix(grid: Grid, loop=False):
    num_walkable = grid.item_counts[GARDEN_PLOT] + grid.item_counts[START]
    start_pos = grid.find(START)
    plot_pos = list(grid.find_all(GARDEN_PLOT))
    pos_to_idx = {pos: i for i, pos in enumerate([start_pos] + plot_pos)}
    # Make adjacency matrix
    adj = lil_matrix((num_walkable, num_walkable), dtype=int)
    for i, pos in enumerate([start_pos] + plot_pos):
        for neighbor in grid.neighbors(pos, loop=loop):
            if grid[neighbor] == GARDEN_PLOT or grid[neighbor] == START:
                adj[i, pos_to_idx[neighbor]] = 1
                adj[pos_to_idx[neighbor], i] = 1
    return adj.tocsr()


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
