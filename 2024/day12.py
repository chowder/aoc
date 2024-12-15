import itertools
import types

Farm = list[str]
Vec2D = tuple[int, int]

c = types.SimpleNamespace()
c.UP = (-1, 0)
c.DOWN = (1, 0)
c.LEFT = (0, -1)
c.RIGHT = (0, 1)


def add(left: Vec2D, right: Vec2D) -> Vec2D:
    return left[0] + right[0], left[1] + right[1]


def same_plant(farm: Farm, pos: Vec2D, direction: Vec2D) -> bool:
    ny, nx = add(pos, direction)
    if ny >= len(farm) or ny < 0 or nx >= len(farm[0]) or nx < 0:
        return False
    current_plant = farm[pos[0]][pos[1]]
    next_plant = farm[ny][nx]
    return next_plant == current_plant


def is_outer_corner(farm: Farm, cell: Vec2D, dir1: Vec2D, dir2: Vec2D) -> bool:
    return (not same_plant(farm, cell, dir1)
            and not same_plant(farm, cell, dir2))


def is_inner_corner(farm: Farm, cell: Vec2D, dir1: Vec2D, dir2: Vec2D) -> bool:
    return (same_plant(farm, cell, dir1)
            and same_plant(farm, cell, dir2)
            and not same_plant(farm, cell, add(dir1, dir2)))


def count_corners(farm: Farm, cell: Vec2D) -> int:
    count = 0

    for d1, d2 in [
        (c.UP, c.RIGHT),  # top-right
        (c.UP, c.LEFT),  # top-left
        (c.DOWN, c.RIGHT),  # bottom-right
        (c.DOWN, c.LEFT),  # bottom-left
    ]:
        count += is_outer_corner(farm, cell, d1, d2)
        count += is_inner_corner(farm, cell, d1, d2)

    return count


def traverse(farm: Farm, cell: Vec2D, seen: set[Vec2D]) -> tuple[int, int, int]:
    area, perimeter, corners = 1, 0, 0

    for direction in (c.UP, c.DOWN, c.LEFT, c.RIGHT):
        if same_plant(farm, cell, direction):
            if (next_position := add(cell, direction)) not in seen:
                seen.add(next_position)
                a, p, cs = traverse(farm, next_position, seen)
                area += a
                perimeter += p
                corners += cs
        else:
            perimeter += 1

    corners += count_corners(farm, cell)

    return area, perimeter, corners


def main():
    with open("inputs/day12.txt") as f:
        farm = f.read().splitlines()

    cells = list(itertools.product(range(len(farm)), range(len(farm[0]))))
    seen = set()

    silver = gold = 0
    for cell in cells:
        if cell in seen or seen.add(cell):
            continue
        area, perimeter, corners = traverse(farm, cell, seen)
        silver += area * perimeter
        gold += area * corners

    print(silver, gold)


if __name__ == "__main__":
    main()
