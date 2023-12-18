from aocd import get_data

import utils
from utils import Grid, Direction
from heapq import heappush, heappop

DAY = 17


def main():
    data = get_data(day=DAY, year=utils.YEAR).splitlines()
    grid = Grid(data)
    # assert part_1(Grid(TEST.splitlines())) == 102
    # part_1(grid)
    assert part_2(Grid(TEST.splitlines())) == 94
    assert part_2(Grid(TEST_2.splitlines())) == 71
    part_2(grid)


def part_1(grid: Grid):
    # Min cost to get from top left to bottom right, only moving at most 3 spaces in one direction consecutively
    cost = 0
    q = []
    seen = set()
    print(grid.bottom_right)
    heappush(q, (int(grid[1, 0]), (1, 0), Direction.SOUTH, 1))
    heappush(q, (int(grid[0, 1]), (0, 1), Direction.EAST, 1))
    while q:
        cost, pos, direction, direction_count = heappop(q)
        # print(cost, pos, direction, direction_count)
        if pos == grid.bottom_right:
            print(cost)
            return cost
        if (pos, direction, direction_count) in seen:
            continue
        seen.add((pos, direction, direction_count))
        for new_direction in Direction.list():
            new_pos = grid.move_point(pos, new_direction)
            if pos == new_pos or new_direction == Direction.opposite(
                direction
            ):  # Invalid direction
                continue
            if direction == new_direction and direction_count < 3:
                heappush(
                    q,
                    (
                        cost + int(grid[new_pos]),
                        new_pos,
                        new_direction,
                        direction_count + 1,
                    ),
                )
            elif direction != new_direction:
                heappush(q, (cost + int(grid[new_pos]), new_pos, new_direction, 1))
    raise ValueError("No path found")


def part_2(grid: Grid):
    # Min cost to get from top left to bottom right, only moving at most 3 spaces in one direction consecutively
    cost = 0
    q = []
    seen = set()
    print(grid.bottom_right)
    heappush(q, (int(grid[1, 0]), (1, 0), Direction.SOUTH, 1))
    heappush(q, (int(grid[0, 1]), (0, 1), Direction.EAST, 1))
    while q:
        cost, pos, direction, direction_count = heappop(q)
        # print(cost, path, direction, direction_count)
        if pos == grid.bottom_right and 4 <= direction_count <= 10:  # Found the end
            print(cost)
            return cost
        # Position visited with this direction already.
        if (pos, direction, direction_count) in seen:
            continue
        seen.add((pos, direction, direction_count))
        if direction_count < 4:  # Need to move in the same direction
            new_pos = grid.move_point(pos, direction)
            if pos != new_pos:
                heappush(
                    q,
                    (
                        cost + int(grid[new_pos]),
                        new_pos,
                        direction,
                        direction_count + 1,
                    ),
                )
            continue
        # Loop through all directions
        for new_direction in Direction.list():
            new_pos = grid.move_point(pos, new_direction)
            # Skip if position is the same (tried to move into wall) or if we are moving in the opposite direction
            if pos == new_pos or new_direction == Direction.opposite(direction):
                continue
            # If we are moving in the same direction, we can only do so 10 times
            elif direction == new_direction and direction_count < 10:
                heappush(
                    q,
                    (
                        cost + int(grid[new_pos]),
                        new_pos,
                        new_direction,
                        direction_count + 1,
                    ),
                )
            elif direction != new_direction:
                # If moving in a new direction, reset direction counter
                heappush(q, (cost + int(grid[new_pos]), new_pos, new_direction, 1))
    raise ValueError("No path found")


TEST = """2413432311323
3215453535623
3255245654254
3446585845452
4546657867536
1438598798454
4457876987766
3637877979653
4654967986887
4564679986453
1224686865563
2546548887735
4322674655533
"""

TEST_2 = """111111111111
999999999991
999999999991
999999999991
999999999991
"""

if __name__ == "__main__":
    main()
