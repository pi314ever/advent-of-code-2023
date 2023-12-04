from utils import get_data_lines


def main():
    lines = get_data_lines("day4.txt")
    assert part_1(lines) == 26426
    assert part_2(lines) == 6227972


def part_1(lines):
    total = 0
    for line in lines:
        card = Card(line)
        total += card.worth()
    print("The total worth of all cards is", total)
    return total


def part_2(lines):
    num_cards = [1 for _ in range(len(lines))]
    num_matches = [0 for _ in range(len(lines))]
    for i, line in enumerate(lines):
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
