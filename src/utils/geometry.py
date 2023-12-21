"Geometry utility functions"


def shoelace_area(vertices: list) -> float:
    """
    Calculate the area of a polygon given its vertices.

    Vertices must be given in clockwise or counter-clockwise order, and none of edges may intersect.
    """
    if vertices[0] != vertices[-1]:
        vertices += [vertices[0]]
    return 0.5 * abs(
        sum(
            [
                vertices[i][0] * vertices[i + 1][1]
                - vertices[i + 1][0] * vertices[i][1]
                for i in range(len(vertices) - 1)
            ]
        )
    )


def picks_theorem(i: int, b: int) -> float:
    """
    Calculate the area of a polygon given the number of interior grid points (i) and the number of boundary grid points (b). All vertices must be on grid points.
    """
    return i + b / 2 - 1


def manhattan_distance(pos1: tuple[int, int], pos2: tuple[int, int]) -> int:
    """Manhattan distance between two points"""
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])


if __name__ == "__main__":
    assert shoelace_area([(0, 0), (1, 0), (1, 1), (0, 1)]) == 1
    assert shoelace_area([(0, 0), (1, 0), (1, 1), (0, 1), (0, 0)]) == 1
    assert shoelace_area([(0, 0), (2, 0), (2, 2), (0, 2)]) == 4
    assert shoelace_area([(0, 0), (3, 0), (3, 3), (0, 3)]) == 9
    assert shoelace_area([(0, 0), (4, 0), (4, 4), (0, 4)]) == 16
    assert shoelace_area([(0, 0), (5, 0), (5, 5), (0, 5)]) == 25
    assert shoelace_area([(0, 0), (3, 0), (3, 4), (2, 8), (0, 2)]) == 16
