import sys
import types

sys.setrecursionlimit(1000000)

c = types.SimpleNamespace()

c.UP = (-1, 0)
c.DOWN = (1, 0)
c.LEFT = (0, -1)
c.RIGHT = (0, 1)

DIRECTIONS = (c.UP, c.DOWN, c.LEFT, c.RIGHT)

add = lambda x, y: tuple(i + j for i, j in zip(x, y))


def can_move(trail, position, direction):
    candidate = add(position, direction)
    tile = trail[candidate[0]][candidate[1]]

    if tile in "<>^v":
        tile = "."

    match tile, direction:
        case "#", _: return False
        case "O", _: return False
        case ".", _: return True
        case ">", c.RIGHT: return True
        case "<", c.LEFT: return True
        case "v", c.DOWN: return True
        case "^", c.UP: return True
        case _: return False


def main():
    with open("inputs/day23.txt") as f:
        trail = [list(l.strip()) for l in f.readlines()]

    trail[0][1] = "#"
    START = (1, 1)
    END = (len(trail) - 2, len(trail[-1]) - 2)

    def traverse(hike, position) -> int:
        if position == END:
            return 1

        tile = hike[position[0]][position[1]]
        max_steps = None

        for direction in DIRECTIONS:
            if can_move(hike, position, direction):
                hike[position[0]][position[1]] = "O"
                steps = traverse(hike, add(position, direction))
                hike[position[0]][position[1]] = tile
                if steps is not None:
                    max_steps = max(max_steps, steps + 1) if max_steps is not None else steps + 1

        return max_steps

    print(traverse(trail, START) + 1)


if __name__ == "__main__":
    main()
