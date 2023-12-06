import math
from functools import reduce
from operator import mul


def ways(t, d):
    hi = (t + math.sqrt((t ** 2) - 4 * d)) / 2
    lo = (t - math.sqrt((t ** 2) - 4 * d)) / 2

    hi = int(math.ceil(hi - 1))
    lo = int(lo + 1)

    return (hi - lo) + 1


def main():
    with open("inputs/day06.txt") as f:
        lines = f.read().splitlines()

    times = [t for t in lines[0].split(":")[1].split(" ") if t]
    distances = [d for d in lines[1].split(":")[1].split(" ") if d]

    print(reduce(mul, [ways(int(t), int(d)) for t, d in zip(times, distances)]))  # Silver
    print(ways(int("".join(times)), int("".join(distances))))  # Gold


if __name__ == "__main__":
    main()
