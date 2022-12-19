from collections import deque, defaultdict


def main():
    with open("inputs/day18.txt") as f:
        cubes = set([tuple(map(int, line.split(","))) for line in f.read().splitlines()])

    directions = (
        (1, 0, 0),
        (-1, 0, 0),
        (0, 1, 0),
        (0, -1, 0),
        (0, 0, 1),
        (0, 0, -1),
    )

    q = deque()
    seen = set([])
    total = 0
    air = defaultdict(int)

    # Silver
    while unseen := (cubes - seen):
        q.append(next(iter(unseen)))
        while q:
            if (cube := q.popleft()) in seen:
                continue
            adj = [(cube[0] + dx, cube[1] + dy, cube[2] + dz) for dx, dy, dz in directions]
            q.extend(c := [n for n in adj if n in cubes])
            for n in adj:
                if n not in cubes:
                    air[n] += 1
            total += 6 - len(c)
            seen.add(cube)

    print(total)

    # Gold
    min_x, max_x = min(x for x, _, _ in cubes) - 1, max(x for x, _, _ in cubes) + 1
    min_y, max_y = min(y for _, y, _ in cubes) - 1, max(y for _, y, _ in cubes) + 1
    min_z, max_z = min(z for _, _, z in cubes) - 1, max(z for _, _, z in cubes) + 1

    seen = set([])
    exterior = 0
    q = deque([(0, 0, 0)])
    while q:
        if (cube := q.popleft()) in seen \
                or cube[0] > max_x or cube[0] < min_x \
                or cube[1] > max_y or cube[1] < min_y \
                or cube[2] > max_z or cube[2] < min_z:
            continue
        adj = [(cube[0] + dx, cube[1] + dy, cube[2] + dz) for dx, dy, dz in directions]
        q.extend((c := [n for n in adj if n not in cubes]))
        exterior += 6 - len(c)
        seen.add(cube)

    print(exterior)


if __name__ == "__main__":
    main()
