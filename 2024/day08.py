import itertools

Vec2D = tuple[int, int]


def add(a: Vec2D, b: Vec2D) -> Vec2D:
    return a[0] + b[0], a[1] + b[1]


def subtract(a: Vec2D, b: Vec2D) -> Vec2D:
    return a[0] - b[0], a[1] - b[1]


def get_antinodes(a: Vec2D, b: Vec2D) -> tuple[Vec2D, Vec2D]:
    return add(b, d := subtract(b, a)), subtract(a, d)


def get_resonant_antinodes(a: Vec2D, b: Vec2D, width: int, height: int):
    yield a
    yield b

    d = subtract(b, a)
    for op, n in ((add, b), (subtract, a)):
        while (n := op(n, d)) and in_bounds(n, width, height):
            yield n


def in_bounds(v: Vec2D, width: int, height: int) -> bool:
    return (0 <= v[0] < height) and (0 <= v[1] < width)


def main():
    with open("inputs/day08.txt") as f:
        city = f.read().splitlines()

    points = [((i, j), city[i][j]) for i in range(len(city)) for j in range(len(city[i]))]
    points = sorted(points, key=lambda p: p[1])  # itertools.groupy requires the input to be sorted
    antennas = {
        k: [p for p, _ in group]
        for k, group in itertools.groupby(points, lambda p: p[1])
        if k != "."
    }
    width, height = len(city[0]), len(city)

    silver, gold = set(), set()
    for i, (_, nodes) in enumerate(antennas.items()):
        for a, b in itertools.combinations(nodes, 2):
            silver.update(get_antinodes(a, b))
            gold.update(get_resonant_antinodes(a, b, width, height))

    silver = list(filter(lambda n: in_bounds(n, width, height), silver))

    print(len(silver))
    print(len(gold))


if __name__ == "__main__":
    main()
