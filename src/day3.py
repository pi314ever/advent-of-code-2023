from aocd import get_data

import utils

DAY = 3


def main():
    data = get_data(day=DAY, year=utils.YEAR).splitlines()
    grid = Grid(data)
    assert part_1(grid) == 550064
    assert part_2(grid) == 85010461


def part_1(grid: "Grid"):
    total = 0
    for k, v in grid.num_adj.items():
        if len(v) > 0:
            total += int(k[2])
    print("The sum of all part numbers is:", total)
    return total


def part_2(grid: "Grid"):
    total = 0
    for k, v in grid.symbol_adj.items():
        if k[2] == "*" and len(v) == 2:
            total += int(v[0]) * int(v[1])
    print("The sum of all gear ratios is:", total)
    return total


def get_full_number(data: list[str], i, j):
    # Find the full number
    current_num = ""
    for j_n in range(j, -1, -1):
        if data[i][j_n].isnumeric():
            current_num = data[i][j_n] + current_num
        else:
            break
    for j_n in range(j + 1, len(data[0])):
        if data[i][j_n].isnumeric():
            current_num += data[i][j_n]
        else:
            break
    return current_num


def is_symbol(c: str):
    return not c.isnumeric() and c != "."


class Grid:
    def __init__(self, data: list[str]):
        self.data = data
        self.N, self.M = len(data), len(data[0]) - 1
        self.neighborhood = utils.GridNeighborhood((self.N, self.M))
        self.symbol_adj = {}  # (i, j, symbol) -> [nums]
        self.num_adj = {}  # (i_start, j_start, num) -> [symbols]
        self.parse()

    def parse(self):
        for i, line in enumerate(self.data):
            line = line.strip()
            j = 0
            # print(line)
            while j < len(line):
                if line[j].isnumeric():
                    # Find the full number
                    current_num = get_full_number(self.data, i, j)
                    # print(current_num)
                    self._add_number_at(i, j, current_num)
                    # Skip ahead
                    j += len(current_num) - 1
                    # input()
                j += 1

    def _add_number_at(self, i, j, num):
        if not self.data[i][j].isnumeric():
            raise ValueError("The character at the given position is not numeric")
        # Find the symbols
        symbols = []
        symbol_pos = []
        for i_n, j_n in self.neighborhood.get_block_neighbors(
            (i, j), (i, j + len(num) - 1), diagonals=True
        ):
            if is_symbol(self.data[i_n][j_n]):
                symbols.append(self.data[i_n][j_n])
                symbol_pos.append((i_n, j_n))
        # Add to the dictionary
        self.num_adj[(i, j, num)] = symbols
        for symbol, pos in zip(symbols, symbol_pos):
            if (pos[0], pos[1], symbol) in self.symbol_adj:
                self.symbol_adj[(pos[0], pos[1], symbol)].append(num)
            else:
                self.symbol_adj[(pos[0], pos[1], symbol)] = [num]


if __name__ == "__main__":
    main()
