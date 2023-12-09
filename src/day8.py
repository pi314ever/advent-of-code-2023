from aocd import get_data
import re
import math

import utils

DAY = 8


def main():
    data = get_data(day=DAY, year=utils.YEAR).splitlines()
    instructions, all_nodes = parse(data)
    assert part_1(instructions, all_nodes) == 20569
    assert part_2(instructions, all_nodes) == 21366921060721


def part_1(instructions: str, all_nodes: dict[str, "Node"]):
    steps = 0
    current_node = all_nodes["AAA"]
    while current_node.value != "ZZZ":
        if instructions[steps % len(instructions)] == "L":
            current_node = current_node.left
        elif instructions[steps % len(instructions)] == "R":
            current_node = current_node.right
        if current_node is None:
            raise ValueError("Invalid instruction")
        steps += 1
    print("Total steps: ", steps)
    return steps


def part_2(instructions: str, all_nodes: dict[str, "Node"]):
    steps = 0
    current_nodes = [node for val, node in all_nodes.items() if val.endswith("A")]
    steps_all: list = [None for _ in range(len(current_nodes))]
    end_nodes = {node for val, node in all_nodes.items() if val.endswith("Z")}
    while any(s is None for s in steps_all):
        new_nodes = []
        for i, node in enumerate(current_nodes):
            if instructions[steps % len(instructions)] == "L":
                new_nodes.append(node.left)
            elif instructions[steps % len(instructions)] == "R":
                new_nodes.append(node.right)
            else:
                raise ValueError("Invalid instruction")
            if new_nodes[-1] in end_nodes and steps_all[i] is None:
                steps_all[i] = steps + 1
        current_nodes = new_nodes
        steps += 1
    # LCM of all steps
    steps = math.lcm(*steps_all)
    print("Total steps: ", steps)
    return steps


def parse(data: list[str]):
    # First line is the left/right instructions
    instructions = data[0]

    # Future lines are BST
    all_nodes = {}  # position -> Node
    for line in data[2:]:
        # Regex parse line ([A-Z]{3}) = \(([A-Z]{3}), ([A-Z]{3})\)
        match = re.match(r"([0-9A-Z]{3}) = \(([0-9A-Z]{3}), ([0-9A-Z]{3})\)", line)
        if not match:
            raise ValueError(f"Invalid line: {line}")
        # Create matched nodes
        parent_data = match.group(1)
        left_data = match.group(2)
        right_data = match.group(3)
        if parent_data not in all_nodes:
            all_nodes[parent_data] = Node(parent_data)
        if left_data not in all_nodes:
            all_nodes[left_data] = Node(left_data)
        if right_data not in all_nodes:
            all_nodes[right_data] = Node(right_data)
        # Link nodes
        all_nodes[parent_data].left = all_nodes[left_data]
        all_nodes[parent_data].right = all_nodes[right_data]
    return instructions, all_nodes


class Node:
    def __init__(self, data, left=None, right=None):
        self.value = data
        self.left = None
        self.right = None

    def __repr__(self):
        return f"Node({self.value}, L: {self.left.value if self.left else None}, R: {self.right.value if self.right else None})"


if __name__ == "__main__":
    main()
