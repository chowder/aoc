import math
import re
import time
from collections import Counter
from dataclasses import dataclass
from turtle import Vec2D

ROBOT_REGEX = re.compile(r"p=(-?\d+),(-?\d+) v=(-?\d+),(-?\d+)")


@dataclass(frozen=True)
class Vec2D:
    x: int
    y: int

    def add(self, other: "Vec2D") -> "Vec2D":
        return Vec2D(self.x + other.x, self.y + other.y)


@dataclass
class Robot:
    p: Vec2D
    v: Vec2D

    @staticmethod
    def from_line(line: str) -> "Robot":
        m = ROBOT_REGEX.match(line)
        p = Vec2D(int(m.group(1)), int(m.group(2)))
        v = Vec2D(int(m.group(3)), int(m.group(4)))
        return Robot(p, v)

    def quadrant(self, width: int, height: int) -> int:
        mid_width, mid_height = (width - 1) // 2, (height - 1) // 2
        if self.p.x == mid_width or self.p.y == mid_height:
            return 0
        if self.p.x < mid_width and self.p.y < mid_height:
            return 1
        if self.p.x < mid_width and self.p.y > mid_height:
            return 2
        if self.p.x > mid_width and self.p.y < mid_height:
            return 3
        if self.p.x > mid_width and self.p.y > mid_height:
            return 4


def move(robot: Robot, times: int, width: int, height: int) -> Robot:
    p = robot.p

    for _ in range(times):
        p = p.add(robot.v)
        x, y = p.x % width, p.y % height
        p = Vec2D(x, y)

    return Robot(p, robot.v)


def display(robots: list[Robot], width: int, height: int):
    c = Counter([r.p for r in robots])
    for y in range(height):
        for x in range(width):
            p = Vec2D(x, y)
            if p in c:
                print(c[p], end="")
            else:
                print(".", end="")
        print()


def safety_factor(robots: list[Robot], width: int, height: int) -> int:
    cnt = Counter([r.quadrant(width, height) for r in robots])
    del cnt[0]
    return math.prod(cnt.values())


def main():
    with open("inputs/day14.txt") as f:
        lines = f.read().splitlines()

    width, height = 101, 103
    robots = [Robot.from_line(l) for l in lines]

    after_100s = [move(r, times=100, width=width, height=height) for r in robots]
    print(safety_factor(after_100s, width=width, height=height))

    seconds = 0
    while True:
        seconds += 1
        robots = [move(r, times=1, width=width, height=height) for r in robots]
        if safety_factor(robots, width=width, height=height) < 100000000:
            display(robots, width, height)
            print(f"{seconds=}")
            break


if __name__ == "__main__":
    main()
