from aocd import get_data
from queue import Queue

import utils
from utils import Direction, GridNeighborhood

DAY = 10


def main():
    data = get_data(day=DAY, year=utils.YEAR).splitlines()
    ans, path = part_1(data)
    part_2(data, path)


def part_1(data: list[str]):
    start = starting_pos(data)
    N, M = len(data), len(data[0])
    grid_neighborhood = GridNeighborhood((N, M))
    # Find positions of next starting pipes
    starting_pipes = []
    for i_n, j_n in grid_neighborhood.get_neighbors(start):
        if Direction.get_from((i_n, j_n), start) in Pipe.CHOICES[data[i_n][j_n]]:
            starting_pipes.append((i_n, j_n))
    # Change start to the right pipe
    data[start[0]] = data[start[0]].replace(
        "S",
        Pipe.from_directions(
            [Direction.get_from(start, (i, j)) for i, j in starting_pipes]
        ),
    )

    # BFS from starting position, adding the neighbors that go into starting position
    q = Queue()
    q.put((*start, 0))
    seen = set()
    max_depth = 0
    while not q.empty():
        i, j, depth = q.get()
        if depth > max_depth:
            max_depth = depth
        if (i, j) in seen:
            continue
        # print("Visiting: ", (i, j), "Pipe: ", data[i][j], "Depth: ", depth)
        seen.add((i, j))
        for d in Pipe.CHOICES[data[i][j]]:
            i_n, j_n = Direction.move((i, j), d)
            q.put((i_n, j_n, depth + 1))
    print("Max depth: ", max_depth)
    return max_depth, seen


def part_2(data: list[str], path: set[tuple[int, int]]):
    N, M = len(data), len(data[0])

    count = 0
    for i, line in enumerate(data):
        parity = 0
        direction = None
        for j, char in enumerate(line):
            if (i, j) not in path and parity % 2:
                print(f"\033[92m{char}\033[0m", end="")
                count += 1
            elif (i, j) in path:
                print(char, end="")
                if char == "|":
                    parity += 1
                    direction = None
                elif char == "-":
                    pass
                else:
                    # Change directions
                    if char in ["L", "F"]:
                        direction = char
                        parity += 1
                    elif char == "7" and direction == "F":
                        parity += 1
                        direction = None
                    elif char == "J" and direction == "L":
                        parity += 1
                        direction = None
            else:
                print(f"\033[94m{char}\033[0m", end="")
        print()
    print("Count: ", count)


def starting_pos(data):
    # Find starting position
    start = None
    for i, line in enumerate(data):
        for j, char in enumerate(line):
            if char == "S":
                start = (i, j)
                break
        if start is not None:
            break
    print("Starting position: ", start)
    if start is None:
        raise ValueError("No starting position found")
    return start


class Pipe:
    CHOICES = {
        "L": {Direction.EAST, Direction.NORTH},
        "|": {Direction.NORTH, Direction.SOUTH},
        "7": {Direction.WEST, Direction.SOUTH},
        "-": {Direction.EAST, Direction.WEST},
        "J": {Direction.NORTH, Direction.WEST},
        "F": {Direction.SOUTH, Direction.EAST},
        ".": set(),
    }

    @staticmethod
    def from_directions(directions):
        directions = set(directions)
        for k, v in Pipe.CHOICES.items():
            if v == directions:
                return k
        raise ValueError("Invalid directions")


if __name__ == "__main__":
    main()
