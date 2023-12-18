from aocd import get_data

import utils
from utils import Grid, Direction, shoelace_area

DAY = 18

TRENCH = "#"
GROUND = "."

DIRECTION_MAP = {
    "R": Direction.EAST,
    "L": Direction.WEST,
    "U": Direction.NORTH,
    "D": Direction.SOUTH,
}

DIRECTION_ARRAY = ["R", "D", "L", "U"]


def main():
    data = get_data(day=DAY, year=utils.YEAR).splitlines()
    test_data = TEST.splitlines()

    instructions, distances, colors = parse(data)
    test_instructions, test_distances, test_colors = parse(test_data)
    # assert part_1(test_instructions, test_distances) == 62
    assert part_1(instructions, distances) == 61661
    # assert part_2(test_colors) == 952408144115
    assert part_2(colors) == 111131796939729


def part_1(instructions, distances):
    # Make a grid
    lava = num_lava(instructions, distances)
    print(lava)
    return lava


def part_2(colors):
    # Parse colors into instructions
    instructions = []
    distances = []
    for color in colors:
        instructions.append(DIRECTION_ARRAY[int(color[-2])])
        distances.append(int(color[2:-2], 16))
    lava = num_lava(instructions, distances)
    print(lava)
    return lava


def num_lava(instructions, distances):
    vertices = []
    vertices.append((0, 0))
    for d, dist in zip(instructions, distances):
        vertices.append(Direction.move(vertices[-1], DIRECTION_MAP[d], dist))
    area = int(shoelace_area(vertices))
    num_boundary = sum(distances)
    num_interior = area - num_boundary / 2 + 1
    return int(num_interior + num_boundary)


def parse(data):
    instructions = []
    distances = []
    colors = []
    for line in data:
        direction, distance, color = line.split()
        instructions.append(direction)
        distances.append(int(distance))
        colors.append(color)
    return instructions, distances, colors


TEST: str = """R 6 (#70c710)
D 5 (#0dc571)
L 2 (#5713f0)
D 2 (#d2c081)
R 2 (#59c680)
D 2 (#411b91)
L 5 (#8ceee2)
U 2 (#caa173)
L 1 (#1b58a2)
U 2 (#caa171)
R 2 (#7807d2)
U 3 (#a77fa3)
L 2 (#015232)
U 2 (#7a21e3)
"""

if __name__ == "__main__":
    main()
