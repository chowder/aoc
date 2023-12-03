import re
from itertools import product


def merge_intervals(intervals):
    merged = []
    for interval in sorted(intervals):
        if not merged or merged[-1][1] < interval[0]:
            merged.append(interval)
        else:
            merged[-1][1] = max(merged[-1][1], interval[1])
    return merged


def main():
    with open("inputs/day15.txt") as f:
        lines = [tuple(map(int, re.findall(r"=(-?\d*)", line))) for line in f]

    radii = {(sx, sy): abs(sx - bx) + abs(sy - by) for sx, sy, bx, by in lines}
    intervals = [[sx - width, sx + width] for sx, sy, bx, by in lines if (width := (radii[sx, sy] - abs(2000000 - sy))) > 0]
    occupied = sum(i[1] - i[0] for i in merge_intervals(intervals))
    print(occupied)

    acs = set([y - x + r + 1 for (x, y), r in radii.items()])   # Top-left:     (y + sx = x + sy + r + 1) -> (y = x + (sy - sx + r + 1))
    acs |= set([y - x - r - 1 for (x, y), r in radii.items()])  # Bottom-right: (y + sx = x + sy - r - 1) -> (y = x + (sy - sx - r - 1))
    bcs = set([x + y + r + 1 for (x, y), r in radii.items()])   # Top-right:    (y - sx = -x + sy + r + 1) -> (y = -x + (sx + sy + r + 1))
    bcs |= set([x + y - r - 1 for (x, y), r in radii.items()])  # Bottom-left:  (y - sx = -x + sy - r - 1) -> (y = -x + (sx + sy - r - 1))

    for a, b in product(acs, bcs):
        px, py = (b - a) // 2, (a + b) // 2
        if 0 < px < 4000000 and 0 < py < 4000000:
            if all(abs(sx - px) + abs(sy - py) > r for (sx, sy), r in radii.items()):
                print(px * 4000000 + py)
                break


if __name__ == "__main__":
    main()
