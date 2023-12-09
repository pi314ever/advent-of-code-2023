from aocd import get_data

import utils

DAY = 9


def main():
    data = get_data(day=DAY, year=utils.YEAR).splitlines()
    histories = parse(data)
    assert part_1(histories) == 1898776583
    assert part_2(histories) == 1100


def part_1(histories):
    total = 0
    for history in histories:
        val, degree = predict(history)
        total += val
    print("Total future predictions: ", total)
    return total


def part_2(histories):
    total = 0
    for history in histories:
        val, degree = predict(history[::-1])
        total += val
    print("Total previous predictions: ", total)
    return total


def parse(data):
    return [[int(num) for num in line.split()] for line in data]


# Standard recursive method
def predict(sequence):
    if all(s == 0 for s in sequence):
        return sequence[-1], -1
    diff_array = []
    for a, b in zip(sequence, sequence[1:]):
        diff_array.append(b - a)
    pred, depth = predict(diff_array)
    return sequence[-1] + pred, depth + 1


if __name__ == "__main__":
    main()
