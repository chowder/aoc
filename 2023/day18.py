from itertools import product

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


def to_instruction(color):
    steps = int(color[2:-2], 16)
    direction = MOVES[{"0": "R", "1": "D", "2": "L", "3": "U"}[color[-2]]]
    return direction, steps


def get_overlap(left, right):
    return max(0, min(left[1], right[1]) - max(left[0], right[0]) + 1)


def get_lava(dig_plan):
    current = (0, 0)
    v_walls = []
    for (dy, dx), steps in dig_plan:
        y, x = current
        ny, nx = y + steps * dy, x + steps * dx
        if dx == 0:
            v_walls.append((x, (y, ny) if y < ny else (ny, y)))
        current = (ny, nx)

    v_walls = sorted(v_walls)  # (x_axis, (from_y, to_y))
    heights = sorted(set(h for _, r in v_walls for h in r))  # y-axis values where interesting things happen

    lava = 0
    previous_walls = []
    for top, bottom in zip(heights, heights[1:]):
        walls = [x for x, (from_y, to_y) in v_walls if from_y <= top and bottom <= to_y]
        walls = list(zip(walls[::2], walls[1::2]))

        lava += sum((bottom - top + 1) * (right - left + 1) for left, right in walls)
        lava -= sum(get_overlap(p, n) for p, n in product(previous_walls, walls))

        previous_walls = walls

    return lava


def main():
    with open("inputs/day18.txt") as f:
        dig_plan = [l.split() for l in f.read().splitlines()]

    dig_plan_1 = [(MOVES[d], int(s)) for d, s, _ in dig_plan]
    dig_plan_2 = [to_instruction(c) for _, _, c in dig_plan]

    print(get_lava(dig_plan_1), get_lava(dig_plan_2))


if __name__ == "__main__":
    main()
