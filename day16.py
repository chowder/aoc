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


def traverse(nodes, dist, rates, start, seen, time_left, rate, memo):
    if m := memo.get(key := (start, seen, time_left)):
        return m

    max_released = time_left * rate
    for node in nodes - (new_seen := seen | {start}):
        if time_left - (d := dist[start, node] + 1) >= 1:
            released = traverse(nodes, dist, rates, node, new_seen, time_left - d, rate + rates[node], memo) + rate * d
            max_released = max(max_released, released)

    memo[key] = max_released
    return max_released


def main():
    with open("inputs/day16.txt") as f:
        lines = [re.findall(r"([A-Z]{2}|\d+)", line) for line in f.read().splitlines()]
        adj = {v[0]: v[2:] for v in lines}
        rates = {v[0]: int(v[1]) for v in lines}
        dist = {(a, b): min_distance(adj, a, b) for a, b in product(adj.keys(), repeat=2) if a != b}

        # Silver
        nodes = set([n for n in adj.keys() if rates[n] > 0])
        print(traverse(nodes, dist, rates, "AA", frozenset(), 30, 0, {}))

        # Gold
        max_release = 0
        splits = [(set(c), nodes - set(c)) for i in range(1, (len(nodes) // 2) + 1) for c in combinations(nodes, i)]
        for mine, elephants in splits:
            mine = traverse(mine, dist, rates, "AA", frozenset(), 26, 0, {})
            elephants = traverse(elephants, dist, rates, "AA", frozenset(), 26, 0, {})
            max_release = max(max_release, mine + elephants)

        print(max_release)


if __name__ == "__main__":
    main()
