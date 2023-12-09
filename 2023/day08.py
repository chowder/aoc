import itertools
import math
import re


def steps(node, directions, network):
    current = node
    steps = 0
    exits = []
    seen = {node: 0}

    for i, d in itertools.cycle(enumerate(directions)):
        current = network[current][0] if d == "L" else network[current][1]
        steps += 1
        if current.endswith("Z"):
            exits.append(steps)
        if (i, current) in seen:
            return steps - seen[(i, current)], seen[(i, current)], exits

        seen[(i, current)] = steps


def main():
    with open("inputs/day08.txt") as f:
        lines = f.read().splitlines()

    directions = lines[0]
    network = {}
    for line in lines[2:]:
        from_node, to_left, to_right = re.match(r"(\w+) = \((\w+), (\w+)\)", line).groups()
        network[from_node] = (to_left, to_right)

    # Silver
    current = "AAA"
    silver = 0
    for d in itertools.cycle(directions):
        current = network[current][0] if d == "L" else network[current][1]
        silver += 1

        if current == "ZZZ":
            break

    print(silver)

    # Gold
    starts = [n for n in network if n.endswith("A")]
    equations = []
    for n in starts:
        cycles_every, offset, exits = steps(n, directions, network)
        assert len(exits) == 1  # Conveniently we only have one exit per cycle?
        equations.append((cycles_every, exits[0]))

    # If you notice the pattern in the results: the first exit happens to be at the length of the cycle
    assert all(cycles_every == exit_at for cycles_every, exit_at in equations)

    print(math.lcm(*[e[0] for e in equations]))


if __name__ == "__main__":
    main()
