import re

Puzzle = list[str]

X, S = re.compile(r"(?=XMAS)"), re.compile(r"(?=SAMX)")


def rotm45(p: Puzzle) -> Puzzle:
    return ["".join([p[r][c] for r in range(len(p)) for c in range(len(p[0])) if c - r == k]) for k in
            range(-len(p) + 1, len(p[0]))]


def rot45(p: Puzzle) -> Puzzle:
    return ["".join([p[r][c] for r in range(len(p)) for c in range(len(p[0])) if r + c == k]) for k in
            range(len(p) + len(p[0]) - 1)]


def rot90(p: Puzzle) -> Puzzle:
    return ["".join(row) for row in zip(*p[::-1])]


def sub_cubes(p: Puzzle):
    for i in range(len(p[0]) - 2):
        for j in range(len(p) - 2):
            c = [list(p[i + r][j:j + 3]) for r in range(3)]
            c[0][1] = c[1][0] = c[1][2] = c[2][1] = "."
            yield ["".join(l) for l in c]


def xmas(p: Puzzle) -> int:
    return sum(len(X.findall(l)) + len(S.findall(l)) for l in p)


def x_mas(sc) -> bool:
    return any("".join(sc := rot90(sc)) == "M.S.A.M.S" for _ in range(4))


def main():
    with open("inputs/day04.txt") as f:
        puzzle = [l.strip() for l in f.readlines()]

    print(sum(xmas(p) for p in (puzzle, rot45(puzzle), rotm45(puzzle), rot90(puzzle))))
    print(sum(x_mas(sc) for sc in sub_cubes(puzzle)))


if __name__ == "__main__":
    main()
