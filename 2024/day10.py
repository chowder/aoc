import types
from typing import Sequence

Topography = list[list[int]]
Vec2D = tuple[int, int]

c = types.SimpleNamespace()
c.UP = (-1, 0)
c.DOWN = (1, 0)
c.LEFT = (0, -1)
c.RIGHT = (0, 1)


def add(left: Vec2D, right: Vec2D) -> Vec2D:
    return left[0] + right[0], left[1] + right[1]


def can_move(topography: Topography, y: int, x: int, dir: Vec2D) -> bool:
    current_height = topography[y][x]
    ny, nx = add((y, x), dir)
    if ny >= len(topography) or ny < 0 or nx >= len(topography[0]) or nx < 0:
        return False
    next_height = topography[ny][nx]
    return (current_height + 1) == next_height


def valid_directions(topography: Topography, y: int, x: int) -> Sequence[Vec2D]:
    for direction in (c.UP, c.DOWN, c.LEFT, c.RIGHT):
        if can_move(topography, y, x, direction):
            yield direction


def traverse(topography: Topography, y: int, x: int) -> tuple[set[Vec2D], int]:
    if topography[y][x] == 9:
        return {(y, x)}, 1

    peaks, rating = set(), 0

    for direction in valid_directions(topography, y, x):
        p, r = traverse(topography, *add((y, x), direction))
        peaks |= p
        rating += r

    return peaks, rating


def main():
    with open("inputs/day10.txt") as f:
        topography = [list(map(int, l)) for l in f.read().splitlines()]

    total = ratings = 0
    for y, row in enumerate(topography):
        for x, cell in enumerate(row):
            if cell == 0:
                peaks, rating = traverse(topography, y, x)
                total += len(peaks)
                ratings += rating

    print(total, ratings)


if __name__ == "__main__":
    main()
