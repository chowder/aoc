def safe(r: list[int]) -> bool:
    d = [i - j for i, j in zip(r, r[1:])]
    return all(1 <= abs(x) <= 3 for x in d) and \
        not min(d) * max(d) <= 0  # magic?


def without_one(r: list[int]):
    for i in range(len(r)): yield r[:i] + r[i + 1:]


def main():
    with open("inputs/day02.txt") as f:
        reports = [list(map(int, l.strip().split())) for l in f.readlines()]

    print(sum(map(safe, reports)))
    print(sum(any(safe(i) for i in without_one(r)) for r in reports))


if __name__ == "__main__":
    main()
