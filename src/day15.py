from aocd import get_data
import re

import utils

DAY = 15


def main():
    data = get_data(day=DAY, year=utils.YEAR).split(",")
    part_1(data)
    part_2(data)


def part_1(data):
    total = 0
    for val in data:
        total += hash(val)
    print(total)
    return total


def part_2(data):
    boxes = [[] for _ in range(256)]
    for val in data:
        add_match = re.match(r"([a-z]+)=[0-9]", val)
        if add_match:
            # Check if already in list
            for i, lens in enumerate(boxes[hash(add_match.group(1))]):
                if lens.startswith(add_match.group(1)):
                    boxes[hash(add_match.group(1))][i] = val
                    break
            else:
                boxes[hash(add_match.group(1))].append(val)
            continue
        remove_match = re.match(r"([a-z]+)-", val)
        if remove_match:
            for lens in boxes[hash(remove_match.group(1))]:
                if lens.startswith(remove_match.group(1)):
                    boxes[hash(remove_match.group(1))].remove(lens)
                    break
    total = 0
    for i, box in enumerate(boxes):
        for j, item in enumerate(box):
            search = re.search(r"([0-9]+)", item)
            if search:
                total += (i + 1) * (j + 1) * int(search.group(1))
    print(total)
    return total


def hash(sequence):
    total = 0
    for c in sequence:
        total += ord(c)
        total *= 17
        total = total % 256
    return total


if __name__ == "__main__":
    main()
