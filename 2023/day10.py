import sys

sys.setrecursionlimit(15000)

ENDS = {
    "|": {"N", "S"},
    "-": {"E", "W"},
    "L": {"N", "E"},
    "J": {"N", "W"},
    "7": {"S", "W"},
    "F": {"S", "E"},
    ".": {},
    "S": {"N", "S", "E", "W"}
}

OPPOSITE = {
    "N": "S",
    "E": "W",
    "S": "N",
    "W": "E",
}

DIRECTIONS = {
    "N": (-1, 0),
    "E": (0, 1),
    "S": (1, 0),
    "W": (0, -1),
}


def can_move_between_tiles(current: str, to: str, direction: str) -> bool:
    return direction in ENDS[current] and OPPOSITE[direction] in ENDS[to]


def is_in_bounds(row, col, sketch) -> bool:
    return 0 <= row < len(sketch) and 0 <= col < len(sketch[0])


def dfs(current: tuple[int, int], sketch, seen, depth):
    print(current)
    current_tile = sketch[current[0]][current[1]]
    seen.add(current)
    for direction, value in DIRECTIONS.items():
        next_row, next_col = current[0] + value[0], current[1] + value[1]

        if is_in_bounds(next_row, next_col, sketch):
            next_tile = sketch[next_row][next_col]
            if next_tile == "S" and depth > 1 and can_move_between_tiles(current_tile, next_tile, direction):
                return current, (next_row, next_col)

            if (next_row, next_col) not in seen and can_move_between_tiles(current_tile, next_tile, direction):
                if path := dfs((next_row, next_col), sketch, seen, depth + 1):
                    return current, *path

    return None


def main():
    with open("inputs/day10.txt") as f:
        sketch = f.read().splitlines()

    current = (row := next(r for r, l in enumerate(sketch) if "S" in l)), sketch[row].index("S")

    path = dfs(current, sketch, set(), 0)
    print((len(path) - 1) / 2)

    for r, line in enumerate(sketch):
        for c, l in enumerate(line):
            if (r, c) in path:
                sys.stdout.write(l)
            else:
                sys.stdout.write(" ")
        sys.stdout.write("\n")


if __name__ == "__main__":
    main()
