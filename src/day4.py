from aocd import get_data

import utils

DAY = 4


def main():
    data = get_data(day=DAY, year=utils.YEAR).splitlines()
    assert part_1(data) == 26426
    assert part_2(data) == 6227972


def part_1(data):
    total = 0
    for line in data:
        card = Card(line)
        total += card.worth()
    print("The total worth of all cards is", total)
    return total


def part_2(data):
    num_cards = [1 for _ in range(len(data))]
    num_matches = [0 for _ in range(len(data))]
    for i, line in enumerate(data):
        card = Card(line)
        num_matches[i] = card.matches
        for j in range(card.matches):
            num_cards[i + j + 1] += num_cards[i]
    print("The total number of cards is", sum(num_cards))
    return sum(num_cards)


class Card:
    def __init__(self, line: str):
        card, numbers = line.split(":")
        self.id = int(card.split()[1])
        winning, owned = numbers.split("|")
        self.winning_numbers = set(int(n) for n in winning.split())
        self.card = set(int(n) for n in owned.split())
        self.matches = len(self.winning_numbers.intersection(self.card))

    def worth(self):
        return 2 ** (self.matches - 1) if self.matches else 0


if __name__ == "__main__":
    main()
