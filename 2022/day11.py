import math
from collections import namedtuple
from functools import reduce, partial
from operator import add, sub, mul, truediv

OPS = {"+": add, "*": mul}
Monkey = namedtuple("Monkey", ["items", "func", "divisor", "if_true", "if_false"])


def main():
    with open("inputs/day11.txt") as f:
        lines = f.read().splitlines()

    for p in ("silver", "gold"):
        monkeys = []
        for group in [lines[i:i + 6] for i in range(0, len(lines), 7)]:
            items = [int(n.strip()) for n in group[1][18:].split(",")]

            match (f := group[2][13:].split()):
                case ["new", "=", "old", str(op), "old"]:
                    o = OPS[op]
                    func = lambda i: o(i, i)
                case ["new", "=", "old", str(op), str(n)]:
                    func = partial(OPS[op], int(n))
            
            monkeys.append(Monkey(items, func, int(group[3][21:]), int(group[4][29:]), int(group[5][30:])))

        lcm = math.lcm(*[m.divisor for m in monkeys], 1)
        inspects = [0] * len(monkeys)
        
        for _ in range(10000 if p == "gold" else 20):
            for i, monkey in enumerate(monkeys):
                for item in monkey.items:
                    worry = monkey.func(item) % lcm if p == "gold" else monkey.func(item) // 3
                    throw_to = monkey.if_false if worry % monkey.divisor else monkey.if_true
                    monkeys[throw_to].items.append(worry)

                inspects[i] += len(monkey.items)
                monkey.items.clear()

        a, b = sorted(inspects)[-2:]
        print(a * b)


if __name__ == "__main__":
    main()
