from aocd import get_data
import math

import utils

DAY = 6


def main():
    data = get_data(day=DAY, year=utils.YEAR).splitlines()
    times, distances = parse(data)
    assert part_1(times, distances) == 5133600
    assert part_2(times, distances) == 40651271


def part_1(times, distances):
    total = 1
    for t, d in zip(times, distances):
        total *= margin(int(t), int(d))
    print("Product of margins: ", total)
    return total


def part_2(times, distances):
    time = int("".join(times))
    distance = int("".join(distances))
    m = margin(time, distance)
    print("Margin: ", m)
    return m


def margin(time, distance):
    # Solve for the root of the quadratic to find the time
    # Equation: x ( time - x ) - distance = 0
    a = -1
    b = time
    c = -distance
    desc = b**2 - 4 * a * c
    if desc <= 0:
        return 0
    roots = (
        (-b - (b**2 - 4 * a * c) ** 0.5) / (2 * a),
        (-b + (b**2 - 4 * a * c) ** 0.5) / (2 * a),
    )
    low = math.ceil(min(roots))
    high = math.floor(max(roots))
    return high - low + 1


def parse(data):
    times = data[0].split(":")[1].split()
    distances = data[1].split(":")[1].split()
    return times, distances


if __name__ == "__main__":
    main()
