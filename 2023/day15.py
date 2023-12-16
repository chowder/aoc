import re
from collections import defaultdict
from functools import reduce


def get_hash(s):
    return reduce(lambda a, c: ((a + ord(c)) * 17) % 256, s, 0)

def main():
    with open("inputs/day15.txt") as f:
        steps = f.read().split(",")

    # Silver
    print(sum(get_hash(s) for s in steps))

    # Gold
    boxes = [{} for _ in range(256)]
    for step in steps:
        match re.match(r"([a-z]+)([-=])(\d*)", step).groups():
            case [label, "-", _]:
                boxes[get_hash(label)].pop(label, None)
            case [label, "=", focal_length]:
                boxes[get_hash(label)][label] = int(focal_length)

    gold = 0
    for box, contents in enumerate(boxes):
        for slot, focal_length in enumerate(contents.values()):
            gold += (box + 1) * (slot + 1) * focal_length

    print(gold)



if __name__ == "__main__":
    main()
