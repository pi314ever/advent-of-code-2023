from aocd import get_data

import utils

DAY = 1


def main():
    data = get_data(day=DAY, year=utils.YEAR).splitlines()
    assert part_1(data) == 55172
    assert part_2(data) == 54925


def part_1(data):
    sum = 0
    for line in data:
        digits = parse_digits(line)
        sum += 10 * digits[0] + digits[-1]
    print("The total sum is: ", sum)
    return sum


def part_2(data):
    sum = 0
    for line in data:
        digits = parse_alpha_digits(line)
        sum += 10 * digits[0] + digits[-1]
    print("The total sum is: ", sum)
    return sum


def parse_digits(line: str):
    return [int(c) for c in line if c.isdigit()]


def parse_alpha_digits(line: str):
    alpha_to_num = {
        "one": 1,
        "two": 2,
        "six": 6,
        "four": 4,
        "five": 5,
        "nine": 9,
        "three": 3,
        "seven": 7,
        "eight": 8,
    }
    digits = []
    # Regex match positions of digits
    for i in range(len(line)):
        if line[i].isdigit():
            digits.append(int(line[i]))
        for word, num in alpha_to_num.items():
            if line[i : i + len(word)] == word:
                digits.append(num)
                break
    return digits


if __name__ == "__main__":
    main()
