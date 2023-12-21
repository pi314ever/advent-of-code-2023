from aocd import get_data
from collections import deque
import math
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

import utils

DAY = 20

FLIP_FLOP_PREFIX = "%"
CONJUNCTION_PREFIX = "&"


def main():
    data = get_data(day=DAY, year=utils.YEAR).splitlines()
    modules = parse(data)
    test_modules = parse(TEST.splitlines())
    test_modules_2 = parse(TEST_2.splitlines())
    # assert part_1(test_modules) == 32000000
    # assert part_1(test_modules_2) == 11687500
    part_1(modules)
    # Reset modules
    modules = parse(data)
    part_2(modules)
    visualize(modules)


def part_1(modules):
    low_pulses, high_pulses = 0, 0
    for _ in range(1000):
        l, h = simulate(modules)
        low_pulses, high_pulses = low_pulses + l, high_pulses + h
    print(f"Low pulses: {low_pulses}, High pulses: {high_pulses}")
    print(f"Product pulses: {low_pulses * high_pulses}")
    return low_pulses * high_pulses


def part_2(modules):
    # Extracted from visualized representations.
    modalities = [
        0b111111111101,
        0b111100001101,
        0b111111101001,
        0b111111111011,
    ]
    print(f"Modalities: {modalities}")
    print(math.prod(modalities))
    return math.prod(modalities)


def visualize(modules):
    modules["rx"] = FlipFlop("rx", [])
    g = create_graph(modules)[0]

    pos = nx.nx_agraph.graphviz_layout(g, prog="sfdp", root="button")
    fig = plt.figure(figsize=(16, 9), dpi=1920 / 16)

    def animate(frame_number):
        fig.clf()
        edge_colors = simulate_with_edge_colors(modules)
        g, color_map = create_graph(modules)
        nx.draw_networkx_nodes(
            g,
            pos=pos,
            node_color=color_map,
        )
        nx.draw_networkx_labels(g, pos=pos, font_family="monospace", font_size=8)
        nx.draw_networkx_edges(
            g,
            pos=pos,
            connectionstyle="arc3,rad=0.1",
            edge_color=edge_colors,
        )
        plt.legend([f"cycle: {frame_number}"])
        return fig

    anim = FuncAnimation(fig, animate, interval=5, frames=0b111111111111)
    anim.save("data/day20_visualize.gif")


def create_graph(modules):
    graph = nx.DiGraph()
    for name, module in modules.items():
        graph.add_node(name)
        for output in module.outputs:
            graph.add_edge(name, output)
    # Create colors
    color_map = []
    for node in graph:
        module = modules[node]
        if module.type == "b":
            color_map.append("blue")
        elif module.type == "c":
            color_map.append("blue")
        elif module.type == "f":
            if module.state:
                color_map.append("green")
            else:
                color_map.append("red")
    return graph, color_map


def simulate_with_edge_colors(modules):
    graph, _ = create_graph(modules)
    l, h = 0, 0
    q = deque()
    q.append(("button", False, "broadcaster"))
    edges = {}
    while q:
        src, signal, dst = q.popleft()
        # print(f"{src}({modules[src].type}) - {signal} -> {dst}")
        if signal:
            edges[(src, dst)] = "green"
        else:
            edges[(src, dst)] = "red"
        if dst not in modules:
            continue
        for s, signal, d in modules[dst].push(src, signal, modules):
            q.append((s, signal, d))
    edge_colors = [edges.get(e, "black") for e in graph.edges()]
    return edge_colors


def simulate(modules: dict[str, "Module"]):
    l, h = 0, 0
    q = deque()
    q.append(("button", False, "broadcaster"))
    seen = set()
    while q:
        src, signal, dst = q.popleft()
        # print(f"{src}({modules[src].type}) - {signal} -> {dst}")
        # if dst in seen:
        #     print(f"Already seen {dst}")
        # seen.add(dst)
        if signal:
            h += 1
        else:
            l += 1
        if dst not in modules:
            continue
        for s, signal, d in modules[dst].push(src, signal, modules):
            q.append((s, signal, d))
    return l, h


def parse(data) -> dict[str, "Module"]:
    modules = {}
    modules["button"] = Broadcaster("button", ["broadcaster"])

    for line in data:
        if line[0] == FLIP_FLOP_PREFIX:
            name = line.split("->")[0].strip()[1:]
            outputs = list(line.split("->")[1].strip().split(","))
            outputs = [o.strip() for o in outputs]
            modules[name] = FlipFlop(name, outputs)
        elif line[0] == CONJUNCTION_PREFIX:
            name = line.split("->")[0].strip()[1:]
            outputs = list(line.split("->")[1].strip().split(","))
            outputs = [o.strip() for o in outputs]
            modules[name] = Conjunction(name, outputs)
        else:
            name = line.split("->")[0].strip()
            outputs = list(line.split("->")[1].strip().split(","))
            outputs = [o.strip() for o in outputs]
            modules[name] = Broadcaster(name, outputs)

    # Set memory for conjunctions
    for name, module in modules.items():
        for output in module.outputs:
            if output in modules and modules[output].type == "c":
                modules[output].memory[name] = False
    return modules


class Module:
    def __init__(self, type: str, name: str, outputs: list[str]):
        self.type = type
        self.name = name
        self.outputs = outputs

    def __repr__(self):
        return f"({self.type}) {self.name} -> {self.outputs}"

    def push(self, src: str, signal: bool, modules) -> list[tuple[str, bool, str]]:
        raise NotImplementedError


class Broadcaster(Module):
    def __init__(self, name, outputs: list):
        super().__init__("b", name, outputs)

    def push(self, src, signal, modules):
        return [(self.name, signal, output) for output in self.outputs]

    def __repr__(self):
        return super().__repr__()


class Conjunction(Module):
    def __init__(self, name, outputs: list):
        super().__init__("c", name, outputs)
        self.memory = {}

    def push(self, src, signal, modules):
        self.memory[src] = signal
        if all(self.memory.values()):
            return [(self.name, False, output) for output in self.outputs]
        return [(self.name, True, output) for output in self.outputs]

    def __repr__(self):
        return f"({self.type}) {self.name} ({self.memory})-> {self.outputs} "


class FlipFlop(Module):
    def __init__(self, name, outputs: list, state=False):
        super().__init__("f", name, outputs)
        self.state = state

    def push(self, src, signal, modules):
        if self.name == "rx" and not signal:
            raise Exception("Found rx low signal")
        if not signal:
            self.state = not self.state
            return [(self.name, self.state, output) for output in self.outputs]
        else:
            return []

    def __repr__(self):
        return f"({self.type}) {self.name} ({self.state})-> {self.outputs} "


TEST = r"""broadcaster -> a, b, c
%a -> b
%b -> c
%c -> inv
&inv -> a"""

TEST_2 = r"""broadcaster -> a
%a -> inv, con
&inv -> b
%b -> con
&con -> output
"""

if __name__ == "__main__":
    main()
