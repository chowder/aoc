import collections
import itertools
import math
from dataclasses import dataclass, field
from enum import auto, Enum
from itertools import groupby
from typing import Any, List, Protocol


def all_equal(iterable):
    g = groupby(iterable)
    return next(g, True) and not next(g, False)


class Pulse(Enum):
    LOW = auto()
    HIGH = auto()


class Module(Protocol):
    dest: List[str] = field(default_factory=list)

    def apply(self, source, pulse: Pulse) -> tuple[tuple[Any, Pulse], ...]:
        raise NotImplementedError


@dataclass
class Broadcaster:
    dest: List[str] = field(default_factory=list)

    def apply(self, source, pulse: Pulse) -> tuple[tuple[str, Pulse], ...]:
        return tuple((d, pulse) for d in self.dest)


@dataclass
class Flipflop:
    dest: List[str] = field(default_factory=list)
    on: bool = False

    def apply(self, source, pulse: Pulse) -> tuple[tuple[str, Pulse], ...]:
        if pulse == Pulse.HIGH:
            return tuple()

        self.on = not self.on
        return tuple((d, Pulse.HIGH if self.on else Pulse.LOW) for d in self.dest)


@dataclass
class Conjunction:
    memory: dict[str, Pulse] = field(default_factory=dict)
    dest: List[str] = field(default_factory=list)

    def apply(self, source, pulse: Pulse) -> tuple[tuple[str, Pulse], ...]:
        self.memory[source] = pulse
        if all(p == Pulse.HIGH for p in self.memory.values()):
            return tuple((d, Pulse.LOW) for d in self.dest)

        return tuple((d, Pulse.HIGH) for d in self.dest)


Message = tuple[str, str, Pulse]


def make_modules(configuration) -> dict[str, Module]:
    # Create modules
    modules_by_name: dict[str, Module] = {}
    for from_module, to_modules in configuration:
        to_modules = to_modules.split(", ")
        if from_module == "broadcaster":
            modules_by_name[name := from_module] = Broadcaster(dest=to_modules)
        elif from_module.startswith("%"):
            modules_by_name[name := from_module[1:]] = Flipflop(dest=to_modules)
        elif from_module.startswith("&"):
            modules_by_name[name := from_module[1:]] = Conjunction(dest=to_modules)
        else:
            raise Exception("???")

    # Wire up sources for conjunctions
    for name, module in modules_by_name.items():
        if type(module) is Conjunction:
            module.memory = {n: Pulse.LOW for n, m in modules_by_name.items() if name in m.dest}

    return modules_by_name


def main():
    with open("inputs/day20.txt") as f:
        configuration = [l.split(" -> ") for l in f.read().splitlines()]

    modules_by_name = make_modules(configuration)

    initial = ("button", "broadcaster", Pulse.LOW)
    stack = [initial] * 1000
    highs, lows = 0, 1000

    # Silver
    while stack:
        from_module, to_module, pulse = stack.pop()

        if to_module not in modules_by_name:
            continue

        module = modules_by_name[to_module]
        for (next_module, next_pulse) in module.apply(from_module, pulse):
            stack.append((to_module, next_module, next_pulse))
            if next_pulse == Pulse.HIGH:
                highs += 1
            elif next_pulse == Pulse.LOW:
                lows += 1

    print(highs * lows)

    # Gold
    modules_by_name = make_modules(configuration)

    # Specific to my input
    feed = "th"
    collectors = {"xn": [], "qn": [], "xf": [], "zl": []}

    def press(presses: int):
        q = collections.deque([initial])
        while q:
            from_module, to_module, pulse = q.popleft()
            if from_module in collectors and to_module == feed and pulse == Pulse.HIGH:
                collectors[from_module].append(presses)

            if to_module not in modules_by_name:
                continue

            module = modules_by_name[to_module]
            for (next_module, next_pulse) in module.apply(from_module, pulse):
                q.append((to_module, next_module, next_pulse))

    for i in itertools.count(start=1):
        press(i)
        if all(len(c) == 2 for c in collectors.values()):
            break

    assert all(min(l, r) == abs(l - r) for l, r in collectors.values())
    print(math.lcm(*[min(l, r) for l, r in collectors.values()]))


if __name__ == "__main__":
    main()
