from itertools import pairwise
from math import copysign

DIRS = {"D": (0, -1), "R": (1, 0), "U": (0, 1), "L": (-1, 0)}


def main():
    knots = [[0, 0] for _ in range(10)]
    visited = [set() for _ in range(9)]
    with open("inputs/day09.txt") as f:
        for d, n in (line.rstrip('\n').split() for line in  f):
            dx, dy = DIRS[d]
            for _ in range(int(n)):
                knots[0] = knots[0][0] + dx, knots[0][1] + dy
                for i, (h, t) in enumerate(pairwise(knots)):
                    if abs(h[0] - t[0]) == 2 or abs(h[1] - t[1]) == 2:
                        t[0] += max(-1, min(h[0] - t[0], 1))
                        t[1] += max(-1, min(h[1] - t[1], 1))
                    visited[i].add((t[0], t[1]))

    print(len(visited[0]))
    print(len(visited[-1]))

if __name__ == "__main__":
    main()
