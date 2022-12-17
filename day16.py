import re
from itertools import product, combinations


def min_distance(adj_dict, start, end):
    queue = [(start, 0)]
    visited = set()

    while queue:
        node, distance = queue.pop(0)
        if node in visited:
            continue
        if node == end:
            return distance
        visited.add(node)
        queue.extend([(adj_node, distance + 1) for adj_node in adj_dict[node]])


def main():
    with open("inputs/day16.txt") as f:
        lines = [re.findall(r"([A-Z]{2}|\d+)", line) for line in f.read().splitlines()]
        adj = {v[0]: v[2:] for v in lines}
        rates = {v[0]: int(v[1]) for v in lines}
        dist = {(a, b): min_distance(adj, a, b) for a, b in product(adj.keys(), repeat=2) if a != b}

        def traverse(nodes, start, seen, minute, rate, released, max_time):
            nonlocal dist, rates

            max_released = released + (max_time - minute + 1) * rate
            for node in nodes - seen:
                if node != start and minute + (d := dist[start, node] + 1) <= max_time:
                    max_released = max(max_released, traverse(nodes, node, seen | {start}, minute + d, rate + rates[node], released + rate * d, max_time))

            return max_released

        # Silver
        nodes = frozenset([n for n in adj.keys() if rates[n] > 0])
        print(traverse(nodes, "AA", frozenset(), 1, 0, 0, 30))

        # Gold
        max_release = 0
        splits = [(frozenset(c), nodes - set(c)) for i in range(1, (len(nodes) // 2) + len(nodes) % 2 + 1) for c in combinations(nodes, i)]
        for mine, elephants in splits:
            mine = traverse(mine, "AA", frozenset(), 1, 0, 0, 26)
            elephants = traverse(elephants, "AA", frozenset(), 1, 0, 0, 26)
            max_release = max(max_release, mine + elephants)

        print(max_release)


if __name__ == "__main__":
    main()
