import collections
import math
from dataclasses import dataclass
from enum import Enum


class Direction(Enum):
    LEFT = (0, -1)
    RIGHT = (0, 1)
    UP = (-1, 0)
    DOWN = (1, 0)


@dataclass
class Blizzard:
    position: tuple[int, int]
    direction: Direction

    def move(self, height, width):
        y, x = self.position
        dy, dx = self.direction.value
        y, x = (y + dy), (x + dx)
        if y == 0:
            y = height
        elif y == height + 1:
            y = 1
        if x == 0:
            x = width
        elif x == width + 1:
            x = 1

        return Blizzard((y, x), self.direction)


def get_adjacent(y, x):
    yield y, x
    yield y - 1, x
    yield y + 1, x
    yield y, x + 1
    yield y, x - 1


def get_minutes(start, end, blizzards_by_cycle, valley):
    height, width = len(valley) - 2, len(valley[0]) - 2
    lcm = math.lcm(height, width)
    q = collections.deque([(start, 0)])
    seen = {(start, 0)}

    while q:
        (y, x), minute = q.popleft()
        if (y, x) == end:
            return minute
        blizzards = blizzards_by_cycle[(minute + 1) % lcm]
        for ny, nx in get_adjacent(y, x):
            # Out of bounds
            if not (0 <= ny < len(valley) and 0 <= nx < len(valley[0])):
                continue
            # Moving into a wall
            if valley[ny][nx] == "#":
                continue
            # Been here before
            if ((ny, nx), ((minute + 1) % lcm)) in seen:
                continue
            # Will share square with a blizzard if we move there
            if (ny, nx) in blizzards:
                continue

            seen.add(((ny, nx), ((minute + 1) % lcm)))
            q.append(((ny, nx), minute + 1))


def main():
    with open("inputs/day24.txt") as f:
        valley = f.read().splitlines()

    blizzards = []
    for i, line in enumerate(valley):
        for j, char in enumerate(line):
            match char:
                case "<":
                    direction = Direction.LEFT
                case ">":
                    direction = Direction.RIGHT
                case "^":
                    direction = Direction.UP
                case "v":
                    direction = Direction.DOWN
                case _:
                    continue

            blizzards.append(Blizzard((i, j), direction))

    height, width = len(valley) - 2, len(valley[0]) - 2
    lcm = math.lcm(height, width)

    blizzards_by_cycle = [set(b.position for b in blizzards)]
    for _ in range(1, lcm):
        blizzards = [b.move(height, width) for b in blizzards]
        blizzards_by_cycle.append(set(b.position for b in blizzards))

    start = (0, 1)
    end = len(valley) - 1, len(valley[0]) - 2

    # Go there
    total = 0
    minutes = get_minutes(start, end, blizzards_by_cycle, valley)
    print(minutes)
    total += minutes

    # Come back for food
    current_cycle = (minutes % lcm)
    blizzards_by_cycle = blizzards_by_cycle[current_cycle:] + blizzards_by_cycle[:current_cycle]
    minutes = get_minutes(end, start, blizzards_by_cycle, valley)
    print(minutes)
    total += minutes

    # Go there again
    current_cycle = (minutes % lcm)
    blizzards_by_cycle = blizzards_by_cycle[current_cycle:] + blizzards_by_cycle[:current_cycle]
    minutes = get_minutes(start, end, blizzards_by_cycle, valley)

    print(minutes)
    total += minutes

    print("Total:", total)


if __name__ == "__main__":
    main()
