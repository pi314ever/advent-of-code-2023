from aocd import get_data
import re

import utils

DAY = 19


def main():
    data = get_data(day=DAY, year=utils.YEAR).splitlines()
    workflows, ratings = parse(data)
    test_workflows, test_ratings = parse(TEST.splitlines())
    # assert part_1(test_workflows, test_ratings) == 19114
    part_1(workflows, ratings)
    # assert part_2(test_workflows) == 167409079868000
    part_2(workflows)


def part_1(workflows, ratings):
    total = 0
    for rating in ratings:
        if is_accepted(workflows, rating):
            total += sum(rating.values())
    print(total)
    return total


def part_2(workflows: dict[str, "Workflow"]):
    total = 0
    q = []
    q.append(("in", RatingRange()))
    accepted = []
    rejected = []
    while q:
        current, rating_range = q.pop(0)
        if current == "R":
            rejected.append(rating_range)
            continue
        if current == "A":
            accepted.append(rating_range)
            total += rating_range.count()
            continue
        for rule in workflows[current].rules:
            if len(rule) == 1:
                q.append((rule[0], rating_range))
                continue
            r1, rating_range = rating_range.split(rule)
            q.append((rule[3], r1))
    print(total)
    return total


def is_accepted(workflows: dict[str, "Workflow"], rating):
    current = workflows["in"]
    # print(rating)
    while True:
        # print(current)
        next_part = current.next_part(rating)
        if next_part in ["A", "R"]:
            return next_part == "A"
        current = workflows[next_part]


def parse(data):
    workflows = {}
    ratings = []
    i = 0
    while data[i] != "":
        workflow = Workflow.from_line(data[i])
        workflows[workflow.part] = workflow
        i += 1
    i += 1
    while i < len(data):
        rating = {}
        for s in data[i][1:-1].split(","):
            k, v = s.split("=")
            rating[k] = int(v)
        ratings.append(rating)
        i += 1
    return workflows, ratings


class Workflow:
    OUTER_PATTERN = re.compile(r"([a-z]+){(.*)}")
    RULE_PATTERN = re.compile(r"([a-z]+)([<>])([0-9]+):([a-zA-Z]+)")

    def __init__(self, part, rules):
        self.part = part
        self.rules = rules

    def __repr__(self):
        return f"Workflow({self.part}, {self.rules})"

    @staticmethod
    def from_line(line):
        match = Workflow.OUTER_PATTERN.match(line)
        if match is None:
            raise ValueError(f"Invalid line: {line}")
        part = match.group(1)
        rules_str = match.group(2).split(",")
        rules = []
        for rule in rules_str[:-1]:
            var, operation, value, p = Workflow.RULE_PATTERN.match(rule).groups()  # type: ignore
            rules.append((var, operation, int(value), p))
        rules.append((rules_str[-1],))
        return Workflow(part, rules)

    def next_part(self, rating):
        for rule in self.rules:
            if len(rule) == 1:
                return rule[0]
            if rule[1] == "<":
                if rating[rule[0]] < rule[2]:
                    return rule[3]
            elif rule[1] == ">":
                if rating[rule[0]] > rule[2]:
                    return rule[3]
        raise ValueError(f"No rule matched {rating}")


class RatingRange:
    def __init__(self, x=(1, 4000), m=(1, 4000), a=(1, 4000), s=(1, 4000)):
        self.x = x
        self.m = m
        self.a = a
        self.s = s

    def __repr__(self) -> str:
        return f"RatingRange(x={self.x}, m={self.m}, a={self.a}, s={self.s})"

    def to_dict(self):
        return {"x": self.x, "m": self.m, "a": self.a, "s": self.s}

    @staticmethod
    def from_dict(d):
        tmp = {}
        for k in ["x", "m", "a", "s"]:
            if k not in d:
                raise ValueError(f"Missing key: {k}")
            tmp[k] = tuple(d[k])
        return RatingRange(**tmp)

    def split(
        self, rule: tuple[str, str, int, str]
    ) -> tuple["RatingRange", "RatingRange"]:
        """Splits the rating range into one that matches the rule and one that doesn't."""
        var, operation, value, _ = rule
        accepted = self.to_dict()
        rejected = self.to_dict()
        l, r = accepted[var]
        if operation == "<":
            accepted[var] = (l, value - 1)
            rejected[var] = (value, r)
            return RatingRange.from_dict(accepted), RatingRange.from_dict(rejected)
        elif operation == ">":
            accepted[var] = (value + 1, r)
            rejected[var] = (l, value)
            return RatingRange.from_dict(accepted), RatingRange.from_dict(rejected)

        raise ValueError(f"Invalid operation: {operation}")

    def count(self):
        """Returns the number of distinct combinations in the rule"""
        return (
            (self.x[1] - self.x[0] + 1)
            * (self.m[1] - self.m[0] + 1)
            * (self.a[1] - self.a[0] + 1)
            * (self.s[1] - self.s[0] + 1)
        )


TEST = """px{a<2006:qkq,m>2090:A,rfg}
pv{a>1716:R,A}
lnx{m>1548:A,A}
rfg{s<537:gd,x>2440:R,A}
qs{s>3448:A,lnx}
qkq{x<1416:A,crn}
crn{x>2662:A,R}
in{s<1351:px,qqz}
qqz{s>2770:qs,m<1801:hdj,R}
gd{a>3333:R,R}
hdj{m>838:A,pv}

{x=787,m=2655,a=1222,s=2876}
{x=1679,m=44,a=2067,s=496}
{x=2036,m=264,a=79,s=2244}
{x=2461,m=1339,a=466,s=291}
{x=2127,m=1623,a=2188,s=1013}
"""


if __name__ == "__main__":
    main()
