from aocd import get_data
import networkx as nx
import sys
import matplotlib.pyplot as plt

sys.setrecursionlimit(10000)

import utils
from utils import Grid, Direction

DAY = 23

PATH = "."
FOREST = "#"
SLOPES = {
    "^": Direction.NORTH,  # Slope str to only possible move once on this tile.
    ">": Direction.EAST,
    "v": Direction.SOUTH,
    "<": Direction.WEST,
}

LONGEST_PATH = [
    (0, 1),
    (15, 11),
    (31, 19),
    (65, 7),
    (79, 19),
    (99, 19),
    (127, 41),
    (137, 65),
    (109, 67),
    (99, 29),
    (89, 37),
    (89, 67),
    (61, 63),
    (67, 39),
    (31, 41),
    (15, 35),
    (5, 65),
    (33, 61),
    (35, 77),
    (5, 85),
    (15, 107),
    (43, 129),
    (29, 99),
    (61, 99),
    (61, 131),
    (87, 135),
    (81, 103),
    (75, 75),
    (107, 75),
    (135, 77),
    (127, 113),
    (109, 101),
    (101, 125),
    (123, 129),
    (140, 139),
]


def main():
    test_data = TEST.splitlines()
    test_grid = Grid(test_data)
    assert part_1(test_grid) == 94
    # assert part_2(test_grid) == 154

    data = get_data(day=DAY, year=utils.YEAR).splitlines()
    grid = Grid(data)
    # part_1(grid)
    part_2(grid)


def part_1(grid: Grid):
    # Find start location
    start = 0, grid[0].index(PATH)
    end = grid.N - 1, grid[-1].index(PATH)
    steps = longest_path(start, end, set(), grid)
    print(steps)
    return steps


def part_2(grid: Grid):
    # Find start location
    start = 0, grid[0].index(PATH)
    end = grid.N - 1, grid[-1].index(PATH)
    graph = walk(start, end, grid)
    # Brute force DFS
    # steps = dfs(start, 0, end, set(), graph)
    # print(steps)
    visualize_graph(graph, LONGEST_PATH)
    # return steps


def greedy(start, end, graph):
    cur = start
    dist = 0
    seen = set()
    path = []
    to_remove = None
    while cur != end:
        path.append(cur)
        seen.add(cur)
        candidates = []
        for n in graph.neighbors(cur):
            if n not in seen:
                candidates.append((n, graph[cur][n]["weight"]))
        if not candidates:
            # Backtrack
            to_remove = cur  # Remove from seen after committing next move
            path.pop()
            cur = path.pop()
            dist -= graph[cur][path[-1]]["weight"]
            continue
        candidates.sort(key=lambda x: x[1])
        cur, d = candidates[-1]
        dist += d
        if to_remove:
            seen.remove(to_remove)
            to_remove = None
    return path, dist


def n_opt(start, end, graph, n=2):
    # Performs n-opt max path on graph
    path = greedy(start, end, graph)
    if len(path) < n:
        return path


def dfs(cur, dist, end, seen, graph):
    if cur in seen:
        return 0
    if cur == end:
        return dist
    seen.add(cur)
    candidates = []
    for n in graph.neighbors(cur):
        candidates.append(dfs(n, dist + graph[cur][n]["weight"], end, seen, graph))
    if any(c == 6686 for c in candidates):
        print(cur)
    seen.remove(cur)
    if not candidates:
        return 0
    return max(candidates)


def visualize_graph(graph, path=None):
    pos = {n: (n[1], -n[0]) for n in graph.nodes}
    plt.figure(figsize=(12, 12))
    nx.draw(graph, pos=pos, with_labels=True, font_size=8)
    if path is not None:
        x, y = zip(*path)
        x = [-i for i in x]
        plt.plot(y, x, color="red", label="Longest path = 6686")
        plt.legend()
    labels = nx.get_edge_attributes(graph, "weight")
    nx.draw_networkx_edge_labels(graph, pos=pos, edge_labels=labels, font_size=8)
    plt.gca().set_aspect("equal")
    plt.savefig("day23.png", dpi=500)
    # plt.show()


def longest_path(start, end, path: set, grid: Grid):
    if start in path:  # Found loop
        return 0
    if start == end:
        return len(path)
    # print(start, end, len(path))
    path.add(start)
    # At start, continue in all possible directions
    candidates = []
    if grid[start] in SLOPES:
        neighbors = [grid.move_point(start, SLOPES[grid[start]])]
    else:
        neighbors = grid.neighbors(start)
    for n_pos in neighbors:
        if grid[n_pos] == FOREST or n_pos in path:
            continue
        candidates.append(longest_path(n_pos, end, path.copy(), grid))
    if not candidates:
        return 0
    return max(candidates)


def walk(start, end, grid: Grid):
    "Create a grid of node, junctions, and edges weighted by distance."
    q = []
    q.append((0, start, start))
    visited = set()
    graph = nx.Graph()
    graph.add_node(start, pos=start)
    nodes = {start}
    while q:
        dist_from_prev, pos, parent = q.pop()
        if (pos in visited and pos in nodes and pos != parent) or pos == end:
            # Connect parent and pos with distance
            graph.add_edge(parent, pos, weight=dist_from_prev)
            continue
        elif pos in visited:
            continue
        visited.add(pos)
        # Neighbors that are walkable
        neighbors = [n for n in grid.neighbors(pos) if grid[n] != FOREST]
        if len(neighbors) > 2:
            # Found junction, add node and reset parent
            nodes.add(pos)
            graph.add_node(pos, pos=pos)
            graph.add_edge(parent, pos, weight=dist_from_prev)
            parent = pos
            dist_from_prev = 0
        for n in neighbors:
            q.append((dist_from_prev + 1, n, parent))
    return graph


TEST = """#.#####################
#.......#########...###
#######.#########.#.###
###.....#.>.>.###.#.###
###v#####.#v#.###.#.###
###.>...#.#.#.....#...#
###v###.#.#.#########.#
###...#.#.#.......#...#
#####.#.#.#######.#.###
#.....#.#.#.......#...#
#.#####.#.#.#########v#
#.#...#...#...###...>.#
#.#.#v#######v###.###v#
#...#.>.#...>.>.#.###.#
#####v#.#.###v#.#.###.#
#.....#...#...#.#.#...#
#.#########.###.#.#.###
#...###...#...#...#.###
###.###.#.###v#####v###
#...#...#.#.>.>.#.>.###
#.###.###.#.###.#.#v###
#.....###...###...#...#
#####################.#
"""

if __name__ == "__main__":
    main()
