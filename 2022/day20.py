from itertools import product


def main():
    with open("inputs/day20.txt") as f:
        data = [(i, int(l)) for i, l in enumerate(f.read().splitlines())]

    for rounds, key in (1, 1), (10, 811589153):
        original = [(n[0], n[1] * key) for n in data]
        mixed = original[:]
        for _, t in product(range(rounds), original):
            idx = mixed.index(t)
            mixed.pop(idx)
            mixed.insert((idx + t[1]) % len(mixed) or len(mixed), t)

        idx = next(i for i, x in enumerate(mixed) if x[1] == 0)
        coordinates = [mixed[(idx + i) % len(mixed)][1] for i in (1000, 2000, 3000)]
        print(sum(coordinates))


if __name__ == "__main__":
    main()
