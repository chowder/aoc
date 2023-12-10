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


def main():
    with open("inputs/day10.txt") as f:
        sketch = f.read().splitlines()

    start = (row := next(r for r, l in enumerate(sketch) if "S" in l)), sketch[row].index("S")

    # Silver
    row, col = start[0] - 1, start[1]
    direction = "N"
    path = [start, (row, col)]

    while (current_tile := sketch[row][col]) != "S":
        next_direction = next(n for n in ENDS[current_tile] if n != OPPOSITE[direction])
        dy, dx = DIRECTIONS[next_direction]
        row, col = row + dy, col + dx
        direction = next_direction
        path.append((row, col))

    print((len(path) - 1) // 2)

    # Gold
    area = 0
    path = set(path)
    sketch[start[0]] = sketch[start[0]].replace("S", "|")  # Magic

    for row, line in enumerate(sketch):
        inside = 0
        for col, letter in enumerate(line):
            if (row, col) not in path:
                area += inside
            elif sketch[row][col] in {"|", "L", "J"}:
                inside ^= 1

    print(area)


if __name__ == "__main__":
    main()
