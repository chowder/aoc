import collections
import re
from dataclasses import dataclass
from functools import reduce
from itertools import takewhile, dropwhile
from operator import lt, gt, mul
from typing import Optional

Part = dict[str, int]
PartRange = dict[str, tuple[int, int]]


@dataclass
class Condition:
    def matches(self, part: Part) -> bool:
        raise NotImplementedError

    def partition(self, part: PartRange) -> tuple[Optional[PartRange], Optional[PartRange]]:
        raise NotImplementedError


@dataclass
class Compare(Condition):
    category: str
    operator: str
    value: int

    def matches(self, part: Part) -> bool:
        return (lt if self.operator == "<" else gt)(part[self.category], self.value)

    def partition(self, part: PartRange) -> tuple[Optional[PartRange], Optional[PartRange]]:
        lower, upper = part[self.category]
        if self.operator == "<" and lower < self.value:
            return (
                {**part, self.category: (lower, min(upper, self.value - 1))},
                {**part, self.category: (self.value, upper)} if self.value <= upper else None,
            )

        if self.operator == ">" and upper > self.value:
            return (
                {**part, self.category: (max(self.value + 1, lower), upper)},
                {**part, self.category: (lower, self.value)} if lower <= self.value else None,
            )

        return None, None


@dataclass
class Succeed(Condition):
    def matches(self, part: Part) -> bool:
        return True

    def partition(self, part: PartRange) -> tuple[Optional[PartRange], Optional[PartRange]]:
        return part, None


@dataclass
class Statement:
    condition: Condition
    goto: str


Workflow = list[Statement]


def parse_workflow(s) -> tuple[str, Workflow]:
    name, body = re.match(r"(.*){(.*)}", s).groups()
    workflow = []
    for statement in (statements := body.split(","))[:-1]:
        condition, goto = statement.split(":")
        category, op, value = re.match(r"([xmas])([<>])(\d+)", condition).groups()
        workflow.append(Statement(condition=Compare(category, op, int(value)), goto=goto))

    workflow.append(Statement(condition=Succeed(), goto=statements[-1]))
    return name, workflow


def parse_part(s) -> Part:
    return dict([((kv := c.split("="))[0], int(kv[1])) for c in s[1:-1].split(",")])


def main():
    with open("inputs/day19.txt") as f:
        lines = iter(f.read().splitlines())

    workflows, parts = dict([parse_workflow(w) for w in takewhile(lambda l: l, lines)]), [parse_part(s) for s in lines]

    # Silver
    rating = 0
    for part in parts:
        current = "in"
        while current not in {"A", "R"}:
            statement = next(dropwhile(lambda s: not s.condition.matches(part), workflows[current]))
            current = statement.goto

        rating += sum(part.values()) if current == "A" else 0

    print(rating)

    # Gold
    gold = 0
    initial: PartRange = {c: (1, 4000) for c in "xmas"}
    q = collections.deque([("in", initial)])
    while q:
        name, part_range = q.popleft()
        if name in {"A", "R"}:
            gold += reduce(mul, ((r - l + 1) for l, r in part_range.values())) if name == "A" else 0
            continue

        for statement in workflows[name]:
            left, right = statement.condition.partition(part_range)
            left and q.append((statement.goto, left))
            right and q.append((name, right))
            if left or right:
                break

    print(gold)


if __name__ == "__main__":
    main()
