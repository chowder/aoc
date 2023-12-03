import json
from functools import cmp_to_key
from itertools import zip_longest


def compare(l, r):
    for lel, rel in zip_longest(l, r):
        match lel, rel:
            case int(a), int(b):
                if a != b:
                    return a - b
            case list(a), int(b):
                if (res := compare(a, [b])) != 0:
                    return res
            case int(a), list(b):
                if (res := compare([a], b)) != 0:
                    return res
            case list(a), list(b):
                if (res := compare(a, b)) != 0:
                    return res
            case (_, None) | (None, _):
                return -1 if lel is None else 1

    return 0


def main():
    with open("inputs/day13.txt") as f:
        signals = [json.loads(l) for l in f.read().splitlines() if len(l)]

    indices = 0
    for i in range(0, len(signals), 2):
        l, r = signals[i], signals[i+1]
        if compare(l, r) < 0:
            indices += i // 2 + 1

    print(indices)

    dividors = ([[2]], [[6]])
    signals.extend(dividors)

    signals.sort(key=cmp_to_key(compare))

    a = signals.index(dividors[0]) + 1
    b = signals.index(dividors[1]) + 1

    print(a * b)


if __name__ == "__main__":
    main()
