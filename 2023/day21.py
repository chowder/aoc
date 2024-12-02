from itertools import product


def get_adjacent(y, x):
    yield y + 1, x
    yield y - 1, x
    yield y, x + 1
    yield y, x - 1


def main():
    with open("inputs/day21.txt") as f:
        garden = f.read().splitlines()

    start = next((y, x) for y, x in product(range(len(garden)), range(len(garden[0]))) if garden[y][x] == "S")
    current = {start}

    height, width = len(garden), len(garden[0])
    print(height, width)

    def can_visit(y, x):
        # ny, nx = (y % height + height) % height, (x % width + width) % width
        return garden[y % height][x % width] != "#"

    def get_adjacent_zones(from_y, to_y, from_x, to_x):
        yield from_y + height, to_y + height, from_x, to_x
        yield from_y - height, to_y - height, from_x, to_x
        yield from_y, to_y, from_x + width, to_x + width
        yield from_y, to_y, from_x - width, to_x - width

    zones = [(0, height, 0, width)]
    completed_zones = set()
    for i in range(500):
        current = {(ny, nx) for y, x in current for ny, nx in get_adjacent(y, x) if can_visit(ny, nx)}

        new_zones = []
        for zone in zones:
            from_y, to_y, from_x, to_x = zone
            in_zone = {(y, x) for y, x in current if from_y <= y < to_y and from_x <= x < to_x}
            if len(in_zone) in {7354, 7362}:
                print("Completed zone", zone, "at iteration", i, "with", len(in_zone), "in the zone")
                current -= in_zone
                completed_zones.add(zone)
                new_zones.extend([z for z in get_adjacent_zones(from_y, to_y, from_x, to_x) if z not in completed_zones])
            else:
                new_zones.append(zone)

        zones = new_zones

    # 7353, 7362
    print(len(current))


if __name__ == "__main__":
    main()
