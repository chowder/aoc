import itertools
from operator import mul
from functools import reduce


def parse_line(line):
    # All sets cubes ever drawn from the bag
    cubes = sorted([c.split(" ") for r in line.split(": ")[1].split("; ") for c in r.split(", ")], key=lambda c: c[1])
    # Group by the color of the cube
    cubes = [(k, list(g)) for k, g in itertools.groupby(cubes, key=lambda c: c[1])]
    # Highest amount ever drawn for each color
    return {k: max([int(i[0]) for i in g]) for k, g in cubes}


def main():
    with open("inputs/day02.txt") as f:
        lines = f.read().splitlines()

    silver, gold = 0, 0
    for game, line in enumerate(lines):
        cubes = parse_line(line)
        is_possible = cubes["red"] <= 12 and \
                      cubes["green"] <= 13 and \
                      cubes["blue"] <= 14

        silver += (game + 1) if is_possible else 0
        gold += reduce(mul, cubes.values())

    print(silver, gold)


if __name__ == "__main__":
    main()
