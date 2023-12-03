import functools
import heapq


def partition_list(lst, sep):
    part = []
    for e in lst:
        if e == sep:
            yield part
            part = []
        else:
            part.append(e)
    yield part


def main():
    with open("inputs/day01.txt") as f:
        foods = f.read().splitlines()

    elves = [functools.reduce(lambda x, y: x + int(y), calories, 0) for calories in partition_list(foods, "")]
    heapq.heapify(elves)

    print((n_largest := heapq.nlargest(3, elves))[0])  # Silver
    print(sum(n_largest))  # Gold


if __name__ == "__main__":
    main()
