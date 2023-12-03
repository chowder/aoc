from itertools import pairwise, product


def fill(occupied, x, y, maxdepth=float("inf"), floordepth=float("inf")):
    if (x, y) in occupied or y == floordepth:
        return True
    if y >= maxdepth:
        return False
    r = True
    for dx in (0, -1, 1):
        if not (r := r & fill(occupied, x + dx, y + 1, maxdepth, floordepth)):
            break
    if r:
        occupied.add((x, y))
    return r


def main():
    occupied = set()
    with open("inputs/day14.txt") as f:
        for line in f:
            paths = pairwise(tuple(map(int, x.split(","))) for x in line.strip().split(" -> "))
            paths = [sorted(pair) for pair in paths]
            for l, r in paths:
                occupied |= set(product(range(l[0], r[0] + 1), range(l[1], r[1] + 1)))

    depth = max(y for _, y in occupied)
    rocks = len(occupied)

    fill(occupied, 500, 0, maxdepth=depth)
    print(len(occupied) - rocks)

    fill(occupied, 500, 0, floordepth=depth + 2)
    print(len(occupied) - rocks)


if __name__ == "__main__":
    main()
