from functools import reduce
from itertools import pairwise


def main():
    with open("inputs/day09.txt") as f:
        lines = f.read().splitlines()

    silver = 0
    gold = 0

    for line in lines:
        current = [int(i) for i in line.split(" ")]
        next_history = current[-1]
        stack = [current[0]]

        while not current.count(current[0]) == len(current):
            current = [y - x for x, y in pairwise(current)]
            next_history += current[-1]
            stack.append(current[0])

        silver += next_history
        gold += reduce(lambda s, i: i - s, reversed(stack), 0)

    print(silver, gold)


if __name__ == "__main__":
    main()
