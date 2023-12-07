from aocd import get_data

import utils

DAY = 7


def main():
    data = get_data(day=DAY, year=utils.YEAR).splitlines()
    hands = parse(data)
    part_1(hands)
    part_2(hands)


def part_1(hands: list["PokerHand"]):
    # Sort data by hand value
    values_dict = {"A": 14, "K": 13, "Q": 12, "J": 11, "T": 10}
    values_dict.update({str(i): i for i in range(2, 10)})
    for hand in hands:
        hand.set_values(values_dict)
    hands = sorted(hands, key=lambda x: x.value())
    total = 0
    for i, hand in enumerate(hands):
        print(hand, hex(hand.value()), hand.bid)
        total += hand.bid * (i + 1)
    print("Total winnings: ", total)
    return total


def part_2(hands: list["PokerHand"]):
    # Jack is now lowest value of 1
    values_dict = {"A": 14, "K": 13, "Q": 12, "J": 1, "T": 10}
    values_dict.update({str(i): i for i in range(2, 10)})
    for hand in hands:
        hand.set_values(values_dict)
    hands = sorted(hands, key=lambda x: x.value_with_jokers())
    total = 0
    for i, hand in enumerate(hands):
        if "J" in hand.cards:
            print(hand, hex(hand.value_with_jokers()), hand.bid)
        total += hand.bid * (i + 1)
    print("Total winnings: ", total)
    return total


def parse(data):
    hands = []
    for line in data:
        line = line.split()
        cards = [c for c in line[0].strip()]
        hands.append(PokerHand(cards, int(line[1])))
    return hands


class PokerHand:
    def __init__(self, cards: list[str], bid: int):
        self.cards = cards
        self.bid = bid
        assert len(self.cards) == 5, "A poker hand must have 5 cards"

    def set_values(self, values_dict: dict[str, int]):
        self.val2count = {}
        self.count2val = {}
        self.values_dict = values_dict
        for card in self.cards:
            self.val2count[values_dict[card]] = (
                self.val2count.get(values_dict[card], 0) + 1
            )
        for val, count in self.val2count.items():
            self.count2val[count] = self.count2val.get(count, []) + [val]
        map(lambda x: x.sort(reverse=True), self.count2val.values())

    def __repr__(self):
        return f"{self.cards}"

    def _hand_type_value(self):
        if 5 in self.count2val:
            return 0x800000
        if 4 in self.count2val:
            return 0x700000
        if 3 in self.count2val and 2 in self.count2val:
            return 0x600000
        if 3 in self.count2val:
            return 0x500000
        if 2 in self.count2val and len(self.count2val[2]) == 2:
            return 0x400000
        if 2 in self.count2val:
            return 0x300000
        return 0x200000

    def value(self):
        # 6-digit Hex-based number
        # 5 of a kind > 4 of a kind > full house > three of a kind > two pair > one pair > high card
        # 0x{hand type}{cards in order of relevance (high to low)}

        return self._hand_type_value() + sum(
            [self.values_dict[self.cards[i]] * 0x10 ** (4 - i) for i in range(5)]
        )

    def value_with_jokers(self):
        return self._hand_type_with_jokers_value() + sum(
            [self.values_dict[self.cards[i]] * 0x10 ** (4 - i) for i in range(5)]
        )

    def _hand_type_with_jokers_value(self):
        if "J" not in self.cards:
            return self._hand_type_value()
        # Five of a kind given by all jokers or only joker and one other card type
        if 5 in self.count2val or len(self.val2count) == 2:
            return 0x800000
        # Four of a kind given by 3 card types and only 1 card that is not a Joker
        if (
            len(self.val2count) == 3
            and 1 in self.count2val
            and any([c != self.values_dict["J"] for c in self.count2val[1]])
        ):
            return 0x700000
        # Full house given by 3 card types (1 of which is Joker). Only other case of 3 card types is a 4 of a kind, which was already checked
        if len(self.val2count) == 3:
            return 0x600000
        # Three of a kind given by 2 jokers and 3 singles or 1 joker and 1 pair
        if len(self.val2count) == 4:
            return 0x500000
        # Two pairs is not possible with jokers, so only one pair is possible
        if len(self.val2count) == 5:
            return 0x300000
        raise ValueError("Invalid hand type")


if __name__ == "__main__":
    main()
