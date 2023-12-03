from collections import deque
from functools import partial
from itertools import takewhile


def main():
    for l in (4, 14):
        with open("inputs/day06.txt") as f:
            d = deque(maxlen=l)
            s = sum(1 for _ in
                    takewhile(
                        lambda c: d.append(c) or len(set(d)) != l,
                        iter(partial(f.read, 1), '')
                    ))
            print(s + 1)


if __name__ == "__main__":
    main()
