def contains(a, b) -> bool:
    if a[0] >= b[0] and a[1] <= b[1]:
        return True
    if b[0] >= a[0] and b[1] <= a[1]:
        return True
    return False


def has_overlap(a, b) -> bool:
    if a[0] <= b[1] and a[1] >= b[0]:
        return True
    if b[0] <= a[1] and b[1] >= a[0]:
        return True
    return False


def main():
    with open("inputs/day04.txt") as f:
        pairs = [line.strip() for line in f.readlines()]

    pairs = [pair.split(",") for pair in pairs]
    pairs = [(a.split("-"), b.split("-")) for a, b in pairs]
    pairs = [((int(a), int(b)), (int(c), int(d))) for ((a, b), (c, d)) in pairs]

    print(sum(contains(*pair) for pair in pairs))  # Silver
    print(sum(has_overlap(*pair) for pair in pairs))  # Gold


if __name__ == "__main__":
    main()
    
# 10-71 3-4
