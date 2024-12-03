def main():
    with open("inputs/day01.txt") as f:
        l, r = zip(*[map(int, l.strip().split("   ")) for l in f.readlines()])

    print(sum(abs(i - j) for i, j in zip(sorted(l), sorted(r))))
    print(sum(i * r.count(i) for i in l))


if __name__ == "__main__":
    main()
