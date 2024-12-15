import re
from dataclasses import dataclass
from fractions import Fraction
from typing import Optional

BUTTON_REGEX = re.compile(r"Button [AB]: X\+(\d+), Y\+(\d+)")
PRIZE_REGEX = re.compile(r"Prize: X=(\d+), Y=(\d+)")


@dataclass(frozen=True)
class Vec2D:
    x: int
    y: int

    @staticmethod
    def from_button(line: str) -> "Vec2D":
        m = BUTTON_REGEX.match(line)
        return Vec2D(int(m.group(1)), int(m.group(2)))

    @staticmethod
    def from_prize(line: str) -> "Vec2D":
        m = PRIZE_REGEX.match(line)
        return Vec2D(int(m.group(1)), int(m.group(2)))


@dataclass
class Machine:
    a: Vec2D
    b: Vec2D
    prize: Vec2D

    @staticmethod
    def from_lines(lines: tuple[str, str, str]):
        return Machine(
            a=Vec2D.from_button(lines[0]),
            b=Vec2D.from_button(lines[1]),
            prize=Vec2D.from_prize(lines[2]),
        )

    def add_10000000000000(self) -> "Machine":
        return Machine(
            a=self.a,
            b=self.b,
            prize=Vec2D(self.prize.x + 10000000000000, self.prize.y + 10000000000000),
        )


def tokens(machines: list[Machine]) -> int:
    total = 0
    for m in machines:
        if s := solution(m):
            total += s.x * 3 + s.y
    return total


# @formatter:off
def solution(machine: Machine) -> Optional[Vec2D]:
    a = machine.a.x; b = machine.b.x
    c = machine.a.y; d = machine.b.y

    # Inverse the matrix
    det = a * d - b * c
    a1 = Fraction(d, det); b1 = Fraction(-b, det)
    c1 = Fraction(-c, det); d1 = Fraction(a, det)

    x = a1 * machine.prize.x + b1 * machine.prize.y
    y = c1 * machine.prize.x + d1 * machine.prize.y

    if x.is_integer() and y.is_integer():
        return Vec2D(int(x), int(y))

    return None
# @formatter:on

def main():
    with open("inputs/day13.txt") as f:
        lines = f.read().splitlines()

    machines = list(zip(lines[::4], lines[1::4], lines[2::4]))
    machines = [Machine.from_lines(m) for m in machines]

    print(tokens(machines))
    print(tokens([m.add_10000000000000() for m in machines]))


if __name__ == "__main__":
    main()
