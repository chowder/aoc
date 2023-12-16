Position = Direction = tuple[int, int]
Beam = tuple[Position, Direction]


def propagate(direction, position, layout) -> list[Beam]:
    y, x = position
    tile = layout[y][x]
    match direction, tile:
        case (dy, dx), "\\":
            position = (y + dx, x + dy)
            return [(position, (dx, dy))]
        case (dy, dx), "/":
            position = (y - dx, x - dy)
            return [(position, (-dx, -dy))]
        case (0, _), "|":
            return [
                ((y - 1, x), (-1, 0)),  # Up
                ((y + 1, x), (1, 0))  # Down
            ]
        case (_, 0), "-":
            return [
                ((y, x - 1), (0, -1)),  # Left
                ((y, x + 1), (0, 1))  # Right
            ]
        case (dy, dx), _:
            return [((y + dy, x + dx), direction)]
        case _:
            raise Exception("unreachable")


def in_bounds(beam: Beam, layout):
    (y, x), _ = beam
    return 0 <= y < len(layout) and 0 <= x < len(layout[0])


def get_energized(beams: list[Beam], layout):
    seen = set(beams)
    while beams:
        beams = [b for p, d in beams for b in propagate(d, p, layout) if in_bounds(b, layout) and b not in seen]
        seen.update(beams)

    return len(set(p for p, _ in seen))


def main():
    with open("inputs/day16.txt") as f:
        layout = f.read().splitlines()

    # Silver
    beams = [((0, 0), (0, 1))]
    print(get_energized(beams, layout))

    # Gold
    initial = (
            [((0, x), (1, 0)) for x in range(len(layout[0]))] +  # Top
            [((x, 0), (0, 1)) for x in range(len(layout))] +  # Left
            [((x, len(layout[0]) - 1), (0, -1)) for x in range(len(layout))] +  # Right
            [((len(layout) - 1, x), (-1, 0)) for x in range(len(layout))]  # Bottom
    )

    print(max(get_energized([beam], layout) for beam in initial))


if __name__ == "__main__":
    main()
