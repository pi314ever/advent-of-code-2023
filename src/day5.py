from typing import overload

from aocd import get_data

import utils

DAY = 5


def main():
    data = get_data(day=DAY, year=utils.YEAR).splitlines()
    seeds, mappings = parse(data)
    assert part_1(seeds, mappings) == 57075758
    assert part_2(seeds, mappings) == 31161857


def part_1(seeds, mappings):
    min_location = float("inf")
    for seed in seeds:
        # print("Seed:", seed, end=" ")
        for mapping in mappings:
            seed = mapping[seed]
        #     print("->", seed, end=" ")
        # print()
        min_location = min(min_location, seed)
    print("The minimum location is", min_location)
    return min_location


def part_2(seeds, mappings: list["Mapping"]):
    seed_pairs = zip(seeds[::2], seeds[1::2])
    min_location = float("inf")
    for start, length in seed_pairs:
        range = Range(start, start + length)
        ranges = [range]
        # print("Seed:", range, end=" ")
        for mapping in mappings:
            range_copy = [*ranges]
            ranges.clear()
            for r in range_copy:  # Copy and iterate over copy
                ranges.extend(mapping[r])
        #     print("\t->", ranges)
        # print()
        # Loop over all ranges and find the minimum
        for r in ranges:
            min_location = min(min_location, r.start)
    print("The minimum location is", min_location)
    return min_location


def line_to_range(line):
    dest, src, length = map(lambda s: int(s), line.split())
    return (src, src + length), (dest, dest + length)


def parse(lines: list[str]):
    # First line is seeds
    seeds = list(map(lambda s: int(s), lines[0].split()[1:]))
    # Future lines are mappings
    mappings = []
    i = 2
    while i < len(lines):
        # First line of mapping is just label
        i += 1
        m = Mapping()
        while i < len(lines) and lines[i].strip():
            m.add_range(*line_to_range(lines[i].strip()))
            i += 1
        mappings.append(m)
        i += 1
    return seeds, mappings


class Mapping:
    """Defines a mapping from src to dest. Given a src, returns the dest."""

    def __init__(self):
        # Mapping range to a delta operation
        self.range_map: dict["Range", int] = {}

    def add_range(self, src_range, dest_range):
        self.range_map[(Range(*src_range))] = dest_range[0] - src_range[0]

    @overload
    def __getitem__(self, src: int) -> int:
        ...

    @overload
    def __getitem__(self, src: "Range") -> list["Range"]:
        ...

    def __getitem__(self, src):
        if isinstance(src, int):
            return self._get_single(src)
        elif isinstance(src, Range):
            return self._get_range(src)
        raise TypeError(f"Invalid type for src: {type(src)}")

    def _get_single(self, src: int) -> int:
        for r in self.range_map:
            if src in r:
                return self.range_map[r] + src
        return src

    def _get_range(self, src: "Range"):
        result: list["Range"] = []
        range_union = RangeUnion([src])
        for r in self.range_map:
            intersection = r.intersection(src)
            if intersection:
                result.append(intersection.shift(self.range_map[r]))
                range_union.remove(r)
        if len(range_union) > 0:
            result.extend(range_union.ranges)
        # If there is still a range where no intersection was found, add it
        return result


class Range:
    def __init__(self, start, end) -> None:
        # Defines a range from start (inclusive) to end (exclusive)
        self.start = start
        self.end = end

    def __repr__(self) -> str:
        return f"Range({self.start}, {self.end})"

    def length(self):
        return self.end - self.start

    def __len__(self):
        return self.length()

    def __contains__(self, item):
        return self.start <= item < self.end

    def intersection(self, other: "Range"):
        if self.start < other.start:
            start = other.start
        else:
            start = self.start
        if self.end > other.end:
            end = other.end
        else:
            end = self.end
        return Range(start, end) if start < end else None

    def shift(self, delta: int):
        self.start += delta
        self.end += delta
        return self


class RangeUnion:
    def __init__(self, ranges: list[Range]):
        self.ranges = ranges

    def __repr__(self) -> str:
        return f"MultiRange({self.ranges})"

    def __len__(self):
        return sum(len(r) for r in self.ranges)

    def __contains__(self, item):
        return any(item in r for r in self.ranges)

    def remove(self, range: "Range"):
        # Remove the given range from the union
        # This will split ranges if necessary
        new_ranges = []
        for r in self.ranges:
            if r.start >= range.end or r.end <= range.start:
                # No intersection
                new_ranges.append(r)
            elif r.start < range.start < r.end <= range.end:
                # Cut off right side of range
                new_ranges.append(Range(r.start, range.start))
            elif range.start <= r.start <= range.end < r.end:
                # Cut off left side of range
                new_ranges.append(Range(range.end, r.end))
            elif range.start <= r.start and r.end <= range.end:
                # Range is completely contained in r, so remove r
                pass
            elif r.start <= range.start < range.end <= r.end:
                new_ranges.append(Range(r.start, range.start))
                new_ranges.append(Range(range.end, r.end))
            else:
                raise RuntimeError("Invalid range", r, range)
        self.ranges = new_ranges
        return self

    def shift(self, delta: int):
        for r in self.ranges:
            r.shift(delta)
        return self


if __name__ == "__main__":
    main()
