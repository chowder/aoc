import re
from operator import mul
from functools import reduce


def touching(part, symbol):
    return abs(part[0] - symbol[0]) <= 1 and part[1] - 1 <= symbol[1] <= part[2]


def main():
    with open("inputs/day03.txt") as f:
        lines = f.read().splitlines()

    parts = []
    symbols = []
    gears = []
    for row, line in enumerate(lines):
        parts.extend([(int(m.group(0)), (row, m.start(0), m.end(0))) for m in re.finditer(r"\d+", line)])
        symbols.extend([(row, col) for col, c in enumerate(line) if not c.isnumeric() and c != "."])
        gears.extend([(row, col) for col, c in enumerate(line) if c == "*"])

    silver = sum([num for num, p in parts if any(s for s in symbols if touching(p, s))])
    gold = sum([reduce(mul, adjacent) for g in gears if len(adjacent := [num for (num, p) in parts if touching(p, g)]) == 2])

    print(silver, gold)


if __name__ == "__main__":
    main()
