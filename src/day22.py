from aocd import get_data
import json
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.collections import PatchCollection

import utils

DAY = 22

# LINE: x1,y1,z1~x2,y2,z2
# 3D position: (x, y, z)
# Two ends of the brick


def main():
    # test_data = TEST.splitlines()
    # test_bricks = parse(test_data)
    # test_bricks = settle_bricks(test_bricks)
    # assert part_1(test_bricks) == 5
    # assert part_2(test_bricks) == 7

    data = get_data(day=DAY, year=utils.YEAR).splitlines()
    bricks = parse(data)
    bricks = settle_bricks(bricks)
    part_1(bricks)
    part_2(bricks)


def part_1(bricks: list["Brick"]):
    # Iterate through the bricks, and push brick downwards until it hits ground or another brick
    support_map = {}
    for i, brick in enumerate(bricks):
        support_map[brick] = []
        for brick_2 in bricks[:i][::-1]:
            if brick_2.supports(brick):
                support_map[brick].append(brick_2)
    can_remove = {brick: True for brick in bricks}
    for supports in support_map.values():
        if len(supports) == 1:
            can_remove[supports[0]] = False
    num_can_remove = sum(can_remove.values())
    print(num_can_remove)
    return num_can_remove


def part_2(bricks: list["Brick"]):
    support_by_map = {}
    for i, brick in enumerate(bricks):
        support_by_map[brick] = []
        for brick_2 in bricks[:i][::-1]:
            if brick_2.supports(brick):
                support_by_map[brick].append(brick_2)
    supports_map = {}
    for brick, supports in support_by_map.items():
        for support in supports:
            supports_map[support] = supports_map.get(support, []) + [brick]
    can_remove = {brick: True for brick in bricks}
    for supports in support_by_map.values():
        if len(supports) == 1:
            can_remove[supports[0]] = False

    num_supported = {k: len(v) for k, v in support_by_map.items()}

    candidates = [b for b, v in can_remove.items() if not v]
    total = 0
    for candidate in candidates:
        n = num_fall(
            candidate,
            supports_map,
            num_supported.copy(),
        )
        total += n

    print(total)
    return total


def num_fall(brick, supports_map, num_supported):
    q = []
    seen = set()
    total = 0
    q.append(brick)
    while q:
        b = q.pop()
        if b in seen:
            continue
        seen.add(b)
        total += 1
        if b not in supports_map:
            continue
        for support in supports_map[b]:
            num_supported[support] -= 1
            if num_supported[support] == 0:
                q.append(support)
    return max(0, total - 1)


def settle_bricks(bricks: list["Brick"]):
    for i, brick in enumerate(bricks):
        # Find overlapping bricks
        overlap = None
        for brick_2 in bricks[:i][::-1]:
            if brick.xy_box().has_overlap(brick_2.xy_box()):
                if overlap is not None and brick_2.z2 > overlap.z2:
                    overlap = brick_2
                elif overlap is None:
                    overlap = brick_2
        if overlap is None:
            # Set brick to ground level
            brick.descend(brick.z1 - 1)
        else:
            # Set brick to overlap height
            brick.descend(brick.z1 - overlap.z2 - 1)
    return bricks


def plot_bricks(bricks: list["Brick"]):
    max_x = max(brick.x2 for brick in bricks) + 2
    max_y = max(brick.y2 for brick in bricks) + 2
    max_z = max(brick.z2 for brick in bricks) + 2
    fig, (ax1, ax2) = plt.subplots(1, 2)
    ax1.set_aspect("equal")
    ax2.set_aspect("equal")
    print(bricks)
    for i, brick in enumerate(bricks):
        b = patches.Rectangle(
            (brick.x1, brick.z1),
            brick.dx,
            brick.dz,
            linewidth=1,
            edgecolor=(
                i / len(bricks),
                (len(bricks) - i) / len(bricks),
                (len(bricks) - i) / len(bricks),
            ),
            facecolor="none",
        )
        b.set_transform(ax1.transData)
        b.set_clip_on(False)
        ax1.add_patch(b)
        b = patches.Rectangle(
            (brick.y1, brick.z1),
            brick.dy,
            brick.dz,
            linewidth=1,
            edgecolor=(
                i / len(bricks),
                (len(bricks) - i) / len(bricks),
                (len(bricks) - i) / len(bricks),
            ),
            facecolor="none",
        )
        b.set_transform(ax2.transData)
        b.set_clip_on(False)
        ax2.add_patch(b)
    ax1.set_title("XZ view")
    ax2.set_title("YZ view")
    ax1.set_xlim(-1, max_x)
    ax1.set_ylim(-1, max_z)
    ax2.set_xlim(-1, max_y)
    ax2.set_ylim(-1, max_z)
    plt.show()


def parse(data) -> list["Brick"]:
    bricks = []
    for line in data:
        bricks.append(Brick(*[tuple(map(int, p.split(","))) for p in line.split("~")]))  # type: ignore
    bricks.sort(key=lambda b: min(b.z1, b.z2))
    return bricks


class Brick:
    def __init__(self, p1: tuple[int, int, int], p2: tuple[int, int, int]) -> None:
        self.x1, self.x2 = min(p1[0], p2[0]), max(p1[0], p2[0])
        self.y1, self.y2 = min(p1[1], p2[1]), max(p1[1], p2[1])
        self.z1, self.z2 = min(p1[2], p2[2]), max(p1[2], p2[2])

    @property
    def min_corner(self):
        return (self.x1, self.y1, self.z1)

    @property
    def max_corner(self):
        return (self.x2, self.y2, self.z2)

    @property
    def dx(self):
        return self.x2 - self.x1 + 1

    @property
    def dy(self):
        return self.y2 - self.y1 + 1

    @property
    def dz(self):
        return self.z2 - self.z1 + 1

    def xy_box(self):
        return Box((self.x1, self.y1), (self.x2, self.y2))

    def __repr__(self) -> str:
        return f"Brick({self.min_corner}, {self.max_corner})"

    def descend(self, n=1):
        self.z1 -= n
        self.z2 -= n

    def supports(self, other):
        # Returns if this brick supports the other brick directly.
        # Needs to be directly below other brick
        if self.z2 != other.z1 - 1:
            return False
        # Needs to overlap xy boxes
        if not self.xy_box().has_overlap(other.xy_box()):
            return False
        return True

    def copy(self):
        return Brick(self.min_corner, self.max_corner)


class Box:
    def __init__(self, p1, p2) -> None:
        self.x1, self.x2 = min(p1[0], p2[0]), max(p1[0], p2[0])
        self.y1, self.y2 = min(p1[1], p2[1]), max(p1[1], p2[1])

    def has_overlap(self, other):
        # One is above another
        if self.y1 > other.y2 or other.y1 > self.y2:
            return False
        if self.x1 > other.x2 or other.x1 > self.x2:
            return False
        return True


TEST = """1,0,1~1,2,1
0,0,2~2,0,2
0,0,4~0,2,4
2,0,5~2,2,5
0,1,6~2,1,6
0,2,3~2,2,3
1,1,8~1,1,9
"""

if __name__ == "__main__":
    main()
