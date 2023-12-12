from aocd import get_data
from functools import cache

import utils

DAY = 12


def main():
    data = get_data(day=DAY, year=utils.YEAR).splitlines()
    hot_springs, broken_springs = parse(data)
    assert part_1(hot_springs, broken_springs) == 7286
    assert part_2(hot_springs, broken_springs) == 25470469710341


def part_1(hot_springs, broken_springs):
    total = 0
    for hs, bs in zip(hot_springs, broken_springs):
        groups = parse_groups(hs)
        num = num_arrangements(tuple(tuple(g) for g in groups), tuple(bs))
        total += num
    print(total)
    return total


def part_2(hot_springs, broken_springs):
    total = 0
    for hs, bs in zip(hot_springs, broken_springs):
        groups = parse_groups("?".join([hs, hs, hs, hs, hs]))
        num = num_arrangements(tuple(tuple(g) for g in groups), tuple(bs * 5))
        total += num
    print(total)
    return total


def parse_groups(hs):
    # Parse hot springs into islands
    islands = []
    i = 0
    while i < len(hs):
        group = []
        while i < len(hs) and (hs[i] == "#" or hs[i] == "?"):
            group.append(hs[i])
            i += 1
        if group:
            islands.append(group)
        i += 1
    return islands


@cache
def num_arrangements(groups, bs):
    # Count number of ways to arrange the broken springs given the hot springs unknowns
    if not bs and not any("#" in group for group in groups):
        return 1
    if (not groups and bs) or not bs:
        return 0
    # Try to put the first broken spring into first group
    total = 0
    for group in put_broken_spring(groups[0], int(bs[0])):
        n = num_arrangements(
            tuple([group, *groups[1:]]) if group else groups[1:], bs[1:]
        )
        total += n
    # Try to skip the first group
    if "#" not in groups[0]:
        total += num_arrangements(groups[1:], bs)
    return total


def put_broken_spring(group, num_broken_springs):
    # Returns the remainder of all possible ways to put the broken springs into the group
    if num_broken_springs > len(group):
        return
    i = 0
    while i + num_broken_springs <= len(group):
        # Try to put at position i
        if i + num_broken_springs >= len(group) or group[i + num_broken_springs] == "?":
            # Can put spacers on both sides
            yield group[i + num_broken_springs + 1 :]
        if group[i] == "#":
            break
        i += 1


def parse(data):
    hot_springs = []
    broken_springs = []
    for line in data:
        hs, bs = line.split()
        hot_springs.append(hs)
        broken_springs.append(bs.split(","))
    return hot_springs, broken_springs


if __name__ == "__main__":
    main()
