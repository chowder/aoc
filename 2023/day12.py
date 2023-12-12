from functools import cache


@cache
def arrangements(line, groups) -> int:
    if len(line) == 1:
        return 1 if line[0] == "#" and groups == (1,) or line[0] == "." and not groups else 0

    match (line[0], line[1]):
        case "#", ".":
            return arrangements(line[1:], groups[1:]) if groups and groups[0] == 1 else 0
        case "#", "#":
            return arrangements(line[1:], (groups[0] - 1, *groups[1:])) if groups and groups[0] > 0 else 0
        case s, "?":
            damaged = s + "#" + line[2:]
            operational = s + "." + line[2:]
            return arrangements(damaged, groups) + arrangements(operational, groups)
        case ".", _:
            return arrangements(line[1:], groups)


def main():
    with open("inputs/day12.txt") as f:
        lines = f.read().splitlines()

    silver = 0
    gold = 0

    for line in lines:
        row, groups = line.split(" ")
        groups = tuple(int(i) for i in groups.split(","))

        silver += arrangements(f".{row}", groups)
        gold += arrangements(f".{'?'.join([row] * 5)}", groups * 5)

    print(silver, gold)


if __name__ == "__main__":
    main()
