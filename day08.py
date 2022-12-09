from functools import reduce
from itertools import chain
from operator import mul 


def takeuntil(pred, it):
    for el in it:
        yield el
        if not pred(el): 
            break
        

def main():
    with open("inputs/day08.txt") as f: 
        lines = f.read().splitlines()
        trees = [int(t) for t in chain.from_iterable(lines)]

    width = len(lines[0])
    visible, max_score = 0, 0
    
    for i, tree in enumerate(trees):
        l = trees[i - (i % width):i][::-1]
        r = trees[i + 1:(i // width + 1) * width]
        b = trees[i + width::width]
        t = trees[i % width:i:width][::-1]

        if any(map(lambda ts: all(t < tree for t in ts), s := (l, r, t, b))):
            visible += 1

        score = reduce(mul, (sum(1 for _ in takeuntil(lambda t: t < tree, ts)) for ts in s))
        max_score = max(score, max_score)

    print(visible)
    print(max_score)


if __name__ == "__main__":
    main()
