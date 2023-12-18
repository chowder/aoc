import collections
from itertools import accumulate

MOVES = {
    "R": (0, 1),
    "D": (1, 0),
    "L": (0, -1),
    "U": (-1, 0),
}


def get_adjacent(y, x):
    yield y + 1, x
    yield y - 1, x
    yield y, x + 1
    yield y, x - 1


def main():
    with open("inputs/day18.txt") as f:
        dig_plan = [l.split() for l in f.read().splitlines()]

    border = [(0, 0)]
    for direction, steps, color in dig_plan:
        dy, dx = MOVES[direction]
        border.extend(accumulate(range(int(steps)), lambda l, r: (l[0] + dy, l[1] + dx), initial=border[-1]))

    area = set(border)

    assert (start := (1, 1)) not in border

    q = collections.deque([start])
    while q:
        y, x = q.popleft()
        for adj in get_adjacent(y, x):
            if adj not in area:
                area.add(adj)
                q.append(adj)

    print(len(area))


if __name__ == "__main__":
    main()
