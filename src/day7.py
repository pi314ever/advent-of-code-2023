from aocd import get_data

import utils

DAY = 7


def main():
    data = get_data(day=DAY, year=utils.YEAR).splitlines()
    hands = parse(data)
    assert part_1(hands) == 250058342
    assert part_2(hands) == 250506580


def part_1(hands: list["PokerHand"]):
    # Sort data by hand value
    values_dict = {"A": 14, "K": 13, "Q": 12, "J": 11, "T": 10}
    values_dict.update({str(i): i for i in range(2, 10)})
    hands = sorted(hands, key=lambda x: x.value(values_dict))
    total = 0
    for i, hand in enumerate(hands):
        # print(hand, hex(hand.value()), hand.bid)
        total += hand.bid * (i + 1)
    print("Total winnings: ", total)
    return total


def part_2(hands: list["PokerHand"]):
    # Jack is now lowest value of 1
    values_dict = {"A": 14, "K": 13, "Q": 12, "J": 1, "T": 10}
    values_dict.update({str(i): i for i in range(2, 10)})
    hands = sorted(hands, key=lambda x: x.value_with_jokers(values_dict))
    total = 0
    for i, hand in enumerate(hands):
        # if "J" in hand.cards:
        #     print(hand, hex(hand.value_with_jokers()), hand.bid)
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
        self.card2count = {}
        self.count2card = {}
        for card in self.cards:
            self.card2count[card] = self.card2count.get(card, 0) + 1
        for card, count in self.card2count.items():
            self.count2card[count] = self.count2card.get(count, []) + [card]
        map(lambda x: x.sort(reverse=True), self.count2card.values())
        assert len(self.cards) == 5, "A poker hand must have 5 cards"

    def __repr__(self):
        return f"{self.cards}"

    def _hand_type_value(self):
        if 5 in self.count2card:
            return 0x800000
        if 4 in self.count2card:
            return 0x700000
        if 3 in self.count2card and 2 in self.count2card:
            return 0x600000
        if 3 in self.count2card:
            return 0x500000
        if 2 in self.count2card and len(self.count2card[2]) == 2:
            return 0x400000
        if 2 in self.count2card:
            return 0x300000
        return 0x200000

    def value(self, values_dict: dict[str, int]):
        # 6-digit Hex-based number
        # 5 of a kind > 4 of a kind > full house > three of a kind > two pair > one pair > high card
        # 0x{hand type}{cards in order of relevance (high to low)}

        return self._hand_type_value() + sum(
            [values_dict[self.cards[i]] * 0x10 ** (4 - i) for i in range(5)]
        )

    def value_with_jokers(self, values_dict: dict[str, int]):
        return self._hand_type_with_jokers_value() + sum(
            [values_dict[self.cards[i]] * 0x10 ** (4 - i) for i in range(5)]
        )

    def _hand_type_with_jokers_value(self):
        if "J" not in self.cards:
            return self._hand_type_value()
        # Five of a kind given by all jokers or only joker and one other card type
        if 5 in self.count2card or len(self.card2count) == 2:
            return 0x800000
        # Four of a kind given by 3 card types and only 1 card that is not a Joker
        if (
            len(self.card2count) == 3
            and 1 in self.count2card
            and any([c != "J" for c in self.count2card[1]])
        ):
            return 0x700000
        # Full house given by 3 card types (1 of which is Joker). Only other case of 3 card types is a 4 of a kind, which was already checked
        if len(self.card2count) == 3:
            return 0x600000
        # Three of a kind given by 2 jokers and 3 singles or 1 joker and 1 pair
        if len(self.card2count) == 4:
            return 0x500000
        # Two pairs is not possible with jokers, so only one pair is possible
        if len(self.card2count) == 5:
            return 0x300000
        raise ValueError("Invalid hand type")


if __name__ == "__main__":
    main()
