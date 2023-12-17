import heapq
import sys
from dataclasses import dataclass
from enum import Enum
from functools import total_ordering
from typing import TypeAlias, Optional

Point: TypeAlias = tuple[int, int]


class Direction(Enum):
    UP = (-1, 0)
    DOWN = (1, 0)
    LEFT = (0, -1)
    RIGHT = (0, 1)

    def apply_to(self, position: Point) -> Point:
        y, x = position
        dy, dx = self.value
        return y + dy, x + dx


OPPOSITE = {
    Direction.UP: Direction.DOWN,
    Direction.DOWN: Direction.UP,
    Direction.LEFT: Direction.RIGHT,
    Direction.RIGHT: Direction.LEFT,
}


@total_ordering
@dataclass(frozen=True)
class State:
    position: Point
    direction: Optional[Direction]
    count: int

    def __le__(self, other):
        return True


class Crucible(State):
    def get_adjacent(self):
        for direction in (Direction.RIGHT, Direction.DOWN, Direction.UP, Direction.LEFT):
            if self.direction == direction and self.count == 3:
                continue
            if direction == OPPOSITE.get(self.direction):
                continue

            position = direction.apply_to(self.position)
            count = self.count + 1 if direction == self.direction else 1
            yield Crucible(position, direction, count)


class UltraCrucible(State):
    def get_adjacent(self):
        if self.count < 4:
            position = self.direction.apply_to(self.position)
            yield UltraCrucible(position, self.direction, self.count + 1)
        else:
            for direction in (Direction.RIGHT, Direction.DOWN, Direction.UP, Direction.LEFT):
                if direction == self.direction and self.count == 10:
                    continue
                position = direction.apply_to(self.position)
                count = self.count + 1 if direction == self.direction else 1
                yield UltraCrucible(position, direction, count)


def main():
    with open("inputs/day17.txt") as f:
        city = f.read().splitlines()

    height, width = len(city), len(city[0])

    def in_bounds(point: Point):
        return 0 <= point[0] < height and 0 <= point[1] < width

    initial = Crucible(
        position=(0, 0),
        direction=None,
        count=0,
    )

    unvisited = [(0, initial)]
    visited = set()
    distances = {initial: 0}
    while unvisited:
        distance, current = heapq.heappop(unvisited)
        if current.position == (height - 1, width - 1):
            print(distance)
            return

        for adj in current.get_adjacent():
            if adj in visited:
                continue
            if not in_bounds(adj.position):
                continue

            y, x = adj.position
            cost = distance + int(city[y][x])
            if cost < distances.get(adj, sys.maxsize):
                distances[adj] = cost
                heapq.heappush(unvisited, (distances[adj], adj))

        visited.add(current)


if __name__ == "__main__":
    main()
