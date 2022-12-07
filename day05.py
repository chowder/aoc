from itertools import takewhile, filterfalse, product


def main():
    silver = tuple([] for _ in range(9))
    gold = tuple([] for _ in range(9))

    with open("inputs/day05.txt") as f:
        for line in takewhile(lambda l: not l.startswith(" 1"), f):
            crates = filterfalse(lambda x: x[1].isspace(), enumerate(line[1::4]))
            for (i, crate), cargo in product(crates, (silver, gold)):
                cargo[i].insert(0, crate)

        next(f)

        for line in f:
            num, from_, to = (int(x) for x in line.split() if x.isnumeric())
            for i, cargo in enumerate((silver, gold)):
                cargo[to-1].extend(cargo[from_-1][-num:][::1 if i else -1])
                del cargo[from_-1][-num:]

        for cargo in silver, gold:
            print("".join(c[-1] for c in cargo if len(c) > 0))


if __name__ == "__main__":
    main()
