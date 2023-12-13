from functools import cache


def take_patterns(lines):
    pattern = []
    for line in lines:
        if line == '':
            yield tuple(pattern)
            pattern = []
        else:
            pattern.append(line)

    yield tuple(pattern)


@cache
def get_smudges(row, at):
    width = min(at, len(row) - at)
    left = row[max(0, at - width):at]
    right = row[at:at + width]
    return sum(l != r for l, r in zip(left, right[::-1]))


@cache
def get_reflection(pattern, smudges=0):
    for i in range(1, len(pattern[0])):
        if sum(get_smudges(row, i) for row in pattern) == smudges:
            return i
    return 0


def main():
    with open("inputs/day13.txt") as f:
        lines = f.read().splitlines()

    silver = 0
    gold = 0
    for pattern in take_patterns(lines):
        transposed = tuple(''.join(s) for s in zip(*pattern))
        silver += get_reflection(pattern) + get_reflection(transposed) * 100
        gold += get_reflection(pattern, smudges=1) + get_reflection(transposed, smudges=1) * 100

    print(silver, gold)


if __name__ == "__main__":
    main()
