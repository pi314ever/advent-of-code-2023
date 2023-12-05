from dataclasses import dataclass

from aocd import get_data

import utils

DAY = 2


def main():
    data = get_data(day=DAY, year=utils.YEAR).splitlines()
    assert part_1(data) == 2563
    assert part_2(data) == 70768


def part_1(data):
    hand = Cubes(12, 13, 14)
    game = Game(hand)
    sum = 0
    for line in data:
        game.update_game_info(line)
        if game.is_valid():
            sum += game.id
    print("The total sum is: ", sum)
    return sum


def part_2(data):
    game = Game(Cubes(0, 0, 0))
    sum = 0
    for line in data:
        game.update_game_info(line)
        min_bag = game.min_bag()
        sum += min_bag.red * min_bag.green * min_bag.blue
    print("The total sum is: ", sum)
    return sum


@dataclass
class Cubes:
    red: int
    green: int
    blue: int

    def compare_le(self, other):
        return (
            self.red <= other.red
            and self.green <= other.green
            and self.blue <= other.blue
        )

    def compare_ge(self, other):
        return (
            self.red >= other.red
            and self.green >= other.green
            and self.blue >= other.blue
        )

    def max(self, other):
        return Cubes(
            max(self.red, other.red),
            max(self.green, other.green),
            max(self.blue, other.blue),
        )


class Game:
    def __init__(self, bag: Cubes, line=None):
        self.bag = bag
        self.id = -1
        self.grabs = []
        if line:
            self.update_game_info(line)

    def update_game_info(self, line):
        game_info = line.split(":")
        self.id = int(game_info[0].split()[1])  # Game ##: ...
        self.grabs = [self.parse_grab(grab) for grab in game_info[1].split(";")]

    def parse_grab(self, grab: str):
        dice = grab.split(",")
        cubes = {"red": 0, "green": 0, "blue": 0}
        for die in dice:
            value, color = die.split()
            cubes[color] = int(value)
        return Cubes(**cubes)

    def is_valid(self):
        for grab in self.grabs:
            if not self.bag.compare_ge(grab):
                return False
        return True

    def min_bag(self):
        if self.id == -1:
            raise ValueError("Game id not set")
        min_bag = self.bag
        for grab in self.grabs:
            min_bag = min_bag.max(grab)
        return min_bag


if __name__ == "__main__":
    main()
