from aocd import get_data
import networkx as nx

import utils

DAY = 25


def main():
    test_data = TEST.splitlines()
    test_graph = parse(test_data)
    assert part_1(test_graph) == 54

    data = get_data(day=DAY, year=utils.YEAR).splitlines()
    graph = parse(data)
    part_1(graph)


def part_1(graph: nx.Graph):
    cuts, components = nx.stoer_wagner(graph)
    ans = len(components[0]) * len(components[1])
    print(ans)
    return ans


def visualize(graph: nx.Graph):
    import matplotlib.pyplot as plt

    nx.draw(graph, with_labels=True)
    plt.show()


def parse(data) -> nx.Graph:
    graph = nx.Graph()
    for line in data:
        node, neighbors = line.split(": ")
        graph.add_node(node.strip())
        for n in neighbors.split():
            graph.add_edge(node.strip(), n.strip())
    return graph


TEST = """jqt: rhn xhk nvd
rsh: frs pzl lsr
xhk: hfx
cmg: qnr nvd lhk bvb
rhn: xhk bvb hfx
bvb: xhk hfx
pzl: lsr hfx nvd
qnr: nvd
ntq: jqt hfx bvb xhk
nvd: lhk
lsr: lhk
rzs: qnr cmg lsr rsh
frs: qnr lhk lsr
"""

if __name__ == "__main__":
    main()
