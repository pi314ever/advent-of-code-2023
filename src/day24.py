from aocd import get_data
import numpy as np
import math
from sympy import solve, symbols

import utils

DAY = 24


def main():
    test_data = TEST.splitlines()
    test_hailstones = parse(test_data)
    assert part_1(test_hailstones, (7, 27)) == 2
    assert part_2(test_hailstones) == 47

    data = get_data(day=DAY, year=utils.YEAR).splitlines()
    hailstones = parse(data)
    part_1(hailstones)
    part_2(hailstones)


def part_1(
    hailstones: list["Hailstone"],
    test_area: tuple[int, int] = (200000000000000, 400000000000000),
):
    total = 0
    for i, h1 in enumerate(hailstones):
        for h2 in hailstones[:i]:
            intersect = h1.intersect_path_xy(h2)
            if intersect is not None:
                if (
                    test_area[0] <= intersect[0] <= test_area[1]
                    and test_area[0] <= intersect[1] <= test_area[1]
                ):
                    total += 1
    print(total)
    return total


def part_2(hailstones: list["Hailstone"]):
    # The hailstones can be treated as p + vt. Thus, for two hailstones, p1 - p2 = (v2 - v1)t.
    # This means (p1 - p2) and (v2 - v1) are parallel, which have zero cross product.
    # Thus, (p1 - p2) x (v1 - v2) = 0.
    # p1 x v1 = p1 x v2 + p2 x v1 - p2 x v2
    # If p1 and v1 are the position and velocity of the magic hailstone, then we can use a pair of hailstones to create a system of linear equations for p2 and v2.
    h1 = hailstones[0]
    h2 = hailstones[1]
    h3 = hailstones[2]
    mat = create_matrix(
        h1.pos_3d, h1.vel_3d, h2.pos_3d, h2.vel_3d, h3.pos_3d, h3.vel_3d
    )
    print(mat)
    ans = solve_matrix_sympy(mat)
    print(ans)
    return ans


def cross(v1: "POINT_3D_TYPE", v2: "POINT_3D_TYPE") -> "POINT_3D_TYPE":
    "Returns the cross product of two 3d vectors"
    return (
        v1[1] * v2[2] - v1[2] * v2[1],
        v1[2] * v2[0] - v1[0] * v2[2],
        v1[0] * v2[1] - v1[1] * v2[0],
    )


def sum_vec(v1: "POINT_3D_TYPE", v2: "POINT_3D_TYPE") -> "POINT_3D_TYPE":
    "Returns the sum of two 3d vectors"
    return (v1[0] + v2[0], v1[1] + v2[1], v1[2] + v2[2])


def sub_vec(v1: "POINT_3D_TYPE", v2: "POINT_3D_TYPE") -> "POINT_3D_TYPE":
    "Returns the difference of two 3d vectors"
    return (v1[0] - v2[0], v1[1] - v2[1], v1[2] - v2[2])


def create_matrix(p1, v1, p2, v2, p3, v3):
    matrix = np.zeros((6, 7), dtype=int)
    # First three equations are comparing 1 and 2
    dp = sub_vec(p1, p2)
    dv = sub_vec(v2, v1)
    # (v2 - v1) x p term
    matrix[0, 1] = -dv[2]
    matrix[0, 2] = dv[1]
    matrix[1, 0] = dv[2]
    matrix[1, 2] = -dv[0]
    matrix[2, 0] = -dv[1]
    matrix[2, 1] = dv[0]
    # (p1 - p2) x v term
    matrix[0, 4] = -dp[2]
    matrix[0, 5] = dp[1]
    matrix[1, 3] = dp[2]
    matrix[1, 5] = -dp[0]
    matrix[2, 3] = -dp[1]
    matrix[2, 4] = dp[0]
    print(matrix, dp, dv)
    # Next three equations are comparing 1 and 3
    dp = sub_vec(p1, p3)
    dv = sub_vec(v3, v1)
    # (v3 - v1) x p term
    matrix[3, 1] = -dv[2]
    matrix[3, 2] = dv[1]
    matrix[4, 0] = dv[2]
    matrix[4, 2] = -dv[0]
    matrix[5, 0] = -dv[1]
    matrix[5, 1] = dv[0]
    # (p1 - p3) x v term
    matrix[3, 4] = -dp[2]
    matrix[3, 5] = dp[1]
    matrix[4, 3] = dp[2]
    matrix[4, 5] = -dp[0]
    matrix[5, 3] = -dp[1]
    matrix[5, 4] = dp[0]
    # Constant terms
    matrix[:3, 6] = sub_vec(cross(p1, v1), cross(p2, v2))
    matrix[3:, 6] = sub_vec(cross(p1, v1), cross(p3, v3))
    return matrix


def solve_matrix_sympy(matrix):
    x, y, z = symbols("x y z")
    vx, vy, vz = symbols("vx vy vz")
    sol = solve(
        [
            matrix[0, 0] * x
            + matrix[0, 1] * y
            + matrix[0, 2] * z
            + matrix[0, 3] * vx
            + matrix[0, 4] * vy
            + matrix[0, 5] * vz
            - matrix[0, 6],
            matrix[1, 0] * x
            + matrix[1, 1] * y
            + matrix[1, 2] * z
            + matrix[1, 3] * vx
            + matrix[1, 4] * vy
            + matrix[1, 5] * vz
            - matrix[1, 6],
            matrix[2, 0] * x
            + matrix[2, 1] * y
            + matrix[2, 2] * z
            + matrix[2, 3] * vx
            + matrix[2, 4] * vy
            + matrix[2, 5] * vz
            - matrix[2, 6],
            matrix[3, 0] * x
            + matrix[3, 1] * y
            + matrix[3, 2] * z
            + matrix[3, 3] * vx
            + matrix[3, 4] * vy
            + matrix[3, 5] * vz
            - matrix[3, 6],
            matrix[4, 0] * x
            + matrix[4, 1] * y
            + matrix[4, 2] * z
            + matrix[4, 3] * vx
            + matrix[4, 4] * vy
            + matrix[4, 5] * vz
            - matrix[4, 6],
            matrix[5, 0] * x
            + matrix[5, 1] * y
            + matrix[5, 2] * z
            + matrix[5, 3] * vx
            + matrix[5, 4] * vy
            + matrix[5, 5] * vz
            - matrix[5, 6],
        ],
        [x, y, z, vx, vy, vz],
    )
    return sol[x].floor() + sol[y].floor() + sol[z].floor()


def parse(data):
    hailstones = []
    for line in data:
        pos, vel = line.split("@")
        pos = tuple(int(p.strip()) for p in pos.split(","))
        vel = tuple(int(v.strip()) for v in vel.split(","))
        hailstones.append(Hailstone(pos, vel))  # type: ignore
    return hailstones


POINT_3D_TYPE = tuple[int, int, int]


class Hailstone:
    def __init__(self, pos_3d: tuple[int, int, int], vel_3d: tuple[int, int, int]):
        self.pos_3d = pos_3d
        self.vel_3d = vel_3d

    def __repr__(self):
        return f"Hailstone({self.pos_3d}, {self.vel_3d})"

    @property
    def vel_unit(self) -> tuple[float, float, float]:
        mag = math.sqrt(self.vel_3d[0] ** 2 + self.vel_3d[1] ** 2 + self.vel_3d[2] ** 2)
        return self.vel_3d[0] / mag, self.vel_3d[1] / mag, self.vel_3d[2] / mag

    def pos(self, t: float) -> tuple[float, float]:
        return (
            self.pos_3d[0] + self.vel_3d[0] * t,
            self.pos_3d[1] + self.vel_3d[1] * t,
        )

    def intersect_path_xy(self, other: "Hailstone") -> tuple[float, float] | None:
        "Returns time and position of intersection with other, if any"
        # Check if the xy paths intersect
        # Slopes are dy/dx, check if they are equivalent first
        slope_gcd = math.gcd(self.vel_3d[1], self.vel_3d[0])
        dydx_self = self.vel_3d[1] // slope_gcd, self.vel_3d[0] // slope_gcd
        dydx_self_float = dydx_self[0] / dydx_self[1]
        const_self = self.pos_3d[1] - dydx_self_float * self.pos_3d[0]
        slope_gcd = math.gcd(other.vel_3d[1], other.vel_3d[0])
        dydx_other = other.vel_3d[1] // slope_gcd, other.vel_3d[0] // slope_gcd
        dydx_other_float = dydx_other[0] / dydx_other[1]
        const_other = other.pos_3d[1] - dydx_other_float * other.pos_3d[0]
        if dydx_other == dydx_self or dydx_other_float == dydx_self_float:
            return None

        x = (const_other - const_self) / (dydx_self_float - dydx_other_float)
        time_self = (x - self.pos_3d[0]) / self.vel_3d[0]
        time_other = (x - other.pos_3d[0]) / other.vel_3d[0]
        if time_self < 0 or time_other < 0:
            return None
        y = dydx_self_float * x + const_self
        return x, y


TEST = """19, 13, 30 @ -2,  1, -2
18, 19, 22 @ -1, -1, -2
20, 25, 34 @ -2, -2, -4
12, 31, 28 @ -1, -2, -1
20, 19, 15 @  1, -5, -3
"""

if __name__ == "__main__":
    main()
