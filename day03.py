import functools
import itertools
import string
import typing

# https://stackoverflow.com/a/8998040
def grouper(n: int, iterable: typing.Sequence):
    it = iter(iterable)
    while True:
        chunk_it = itertools.islice(it, n)
        try:
            first_el = next(chunk_it)
        except StopIteration:
            return
        yield itertools.chain((first_el,), chunk_it)


@functools.cache
def to_priority(c: str) -> int:
    return string.ascii_letters.index(c) + 1


def main():
    with open("inputs/day03.txt") as f:
        bags = f.read().splitlines()

    # Silver
    compartments = [(set(bag[:len(bag)//2]), set(bag[len(bag)//2:])) for bag in bags]
    extras = [list(a & b)[0] for a, b in compartments]
    print(sum([to_priority(i) for i in extras]))

    # Gold
    badges = [list(set(a) & set(b) & set(c))[0] for a, b, c in grouper(3, bags)]
    print(sum([to_priority(i) for i in badges]))


if __name__ == "__main__":
    main()
