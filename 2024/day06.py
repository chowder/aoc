import os
from concurrent.futures import ThreadPoolExecutor, as_completed

Position = tuple[int, int]
Direction = str
Lab = list[str]


class CycleException(Exception):
    pass


def next_p(p: Position, d: Direction) -> Position:
    match d:
        case "^":
            return p[0] - 1, p[1]
        case ">":
            return p[0], p[1] + 1
        case "<":
            return p[0], p[1] - 1
        case "v":
            return p[0] + 1, p[1]


def rotate(d: Direction) -> Direction:
    return (dirs := "^>v<")[(dirs.index(d) + 1) % len(dirs)]


def move(p: Position, d: Direction, lab: Lab) -> tuple[Position, Direction]:
    np = next_p(p, d)

    match np:
        case (-1, _) | (_, -1):
            raise IndexError("out of bounds")

    match lab[np[0]][np[1]]:
        case "." | "^" | ">" | "<" | "v":
            return np, d
        case "#":
            return p, rotate(d)


def find_start(lab: Lab) -> tuple[Position, Direction]:
    for i, row in enumerate(lab):
        for j, col in enumerate(row):
            if lab[i][j] in "^v<>":
                return (i, j), lab[i][j]
    raise Exception("where is it?")


def traverse(p: Position, d: Direction, lab: Lab) -> set[Position]:
    seen = {(p, d)}
    while True:
        try:
            np, nd = move(p, d, lab)
            if (np, nd) in seen:
                raise CycleException()
            seen.add((p := np, d := nd))
        except IndexError:
            return set(p for p, _ in seen)


def with_obstacle(lab: Lab, obs: Position):
    return [r[:obs[1]] + "#" + r[obs[1] + 1:] if n == obs[0] else r for n, r in enumerate(lab)]


def main():
    with open("inputs/day06.txt") as f:
        lab = f.read().splitlines()

    p, d = find_start(lab)
    print(len(seen := traverse(p, d, lab)))

    # cpu go brrrr
    threads = len(os.sched_getaffinity(0))
    with ThreadPoolExecutor(max_workers=threads) as executor:
        def task(args):
            try:
                return traverse(*args) and 0
            except CycleException:
                return 1

        futures = [executor.submit(task, (p, d, with_obstacle(lab, step))) for step in seen]
        print(sum(future.result() for future in as_completed(futures)))


if __name__ == "__main__":
    main()
