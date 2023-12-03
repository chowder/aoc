import itertools
from collections import Counter

N = (0, -1)
NE = (1, -1)
E = (1, 0)
SE = (1, 1)
S = (0, 1)
SW = (-1, 1)
W = (-1, 0)
NW = (-1, -1)


def count_empty(grid):
    min_x, max_x = min(x for x, _ in grid), max(x for x, _ in grid) + 1
    min_y, max_y = min(y for _, y in grid), max(y for _, y in grid) + 1
    return (max_x - min_x) * (max_y - min_y) - len(grid)


def main():
    with open("inputs/day23.txt") as f:
        elves = {(x, y) for y, line in enumerate(f) for x, c in enumerate(line) if c == "#"}

    considerations = [
        ((N, NE, NW), N),
        ((S, SE, SW), S),
        ((W, NW, SW), W),
        ((E, NE, SE), E),
    ]

    for i in itertools.count(1):
        proposals = {}
        for x, y in elves:
            if all((x + dx, y + dy) not in elves for dx, dy in (N, NE, E, SE, S, SW, W, NW)):
                continue
            for checks, direction in considerations:
                if all((x + dx, y + dy) not in elves for dx, dy in checks):
                    proposals[(x, y)] = (x + direction[0], y + direction[1])
                    break

        if len(proposals) == 0:
            print(i)
            break

        counts = Counter(proposals.values())
        elves = {(proposals[elf] if elf in proposals and counts[proposals[elf]] == 1 else elf) for elf in elves}
        considerations = considerations[1:] + considerations[:1]

        if i == 10:
            print(count_empty(elves))


if __name__ == "__main__":
    main()
