import re

R = (1, 0)
D = (0, 1)
L = (-1, 0)
U = (0, -1)


def score(coordinates, direction):
    row, column = coordinates[1] + 1, coordinates[0] + 1
    return (1000 * row) + (4 * column) + {R: 0, D: 1, L: 2, U: 3}[direction]


def silver(grid, moves):
    max_x = max(len(row) for row in grid)
    row_starts = [next(i for i, c in enumerate(row) if c != " ") for row in grid]
    column_starts = [next(i for i, row in enumerate(grid) if len(row) > x and row[x] != " ") for x in range(max_x)]
    column_ends = [next(y for y in reversed(range(column_starts[x], len(grid))) if len(grid[y]) > x and grid[y][x] != " ") + 1 for x in range(max_x)]

    start = (grid[0].index("."), 0)
    direction = R

    for steps, turn in re.findall(r"(\d+)([LR]?)", moves):
        for _ in range(int(steps)):
            x, y = start[0] + direction[0], start[1] + direction[1]

            if direction[0] != 0:
                if x >= len(grid[y]):
                    x = row_starts[y]
                elif x < row_starts[y]:
                    x = len(grid[y]) - 1

            if direction[1] != 0:
                if y >= column_ends[x]:
                    y = column_starts[x]
                elif y < column_starts[x]:
                    y = column_ends[x] - 1

            if grid[y][x] == "#":
                break

            start = x, y

        if turn:
            direction = (direction[1], -direction[0]) if turn == "L" else (-direction[1], direction[0])

    print(score(start, direction))


def gold(grid, moves):
    # https://i.imgur.com/h8SEhgU.png
    warp_holes = {}
    for x in range(0, 50):
        # Green warp holes
        warp_holes[(50 + x, -1), U] = (0, 150 + x, R)
        warp_holes[(-1, 150 + x), L] = (50 + x, 0, D)
        # Yellow warp holes
        warp_holes[(49, 49 - x), L] = (0, 100 + x, R)
        warp_holes[(-1, 100 + x), L] = (50, 49 - x, R)
        # Cyan warp holes
        warp_holes[(49, 50 + x), L] = (x, 100, D)
        warp_holes[(x, 99), U] = (50, 50 + x, R)
        # Light pink warp holes
        warp_holes[(100 + x, -1), U] = (x, 199, U)
        warp_holes[(x, 200), D] = (100 + x, 0, D)
        # Orange warp holes
        warp_holes[(99 - x, 150), D] = (49, 199 - x, L)
        warp_holes[(50, 199 - x), R] = (99 - x, 149, U)
        # Pink wrap holes
        warp_holes[(150, x), R] = (99, 149 - x, L)
        warp_holes[(100, 149 - x), R] = (149, x, L)
        # Dark blue warp holes
        warp_holes[(149 - x, 50), D] = (99, 99 - x, L)
        warp_holes[(100, 99 - x), R] = (149 - x, 49, U)

    start = (grid[0].index("."), 0)
    direction = R

    for steps, turn in re.findall(r"(\d+)([LR]?)", moves):
        for _ in range(int(steps)):
            x, y = start[0] + direction[0], start[1] + direction[1]
            new_direction = direction

            if (key := ((x, y), direction)) in warp_holes:
                x, y, new_direction = warp_holes[key]

            if grid[y][x] == "#":
                break

            start = x, y
            direction = new_direction

        if turn:
            direction = (direction[1], -direction[0]) if turn == "L" else (-direction[1], direction[0])

    print(score(start, direction))


def main():
    with open("inputs/day22.txt") as f:
        lines = f.read().splitlines()

    grid = lines[:-2]
    moves = lines[-1]

    silver(grid, moves)
    gold(grid, moves)


if __name__ == "__main__":
    main()
