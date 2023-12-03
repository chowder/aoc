from operator import mul, add, sub, truediv

from z3 import Int, Solver, sat


def main():
    s, g = Solver(), Solver()
    with open("inputs/day21.txt") as f:
        lines = [l.split() for l in f.read().splitlines()]

    operations = {"+": add, "-": sub, "*": mul, "/": truediv}
    monkeys = {}

    for line in lines:
        match line:
            case [str(m), str(left), str(op), str(right)]:
                tm = monkeys.setdefault(m[:-1], Int(m[:-1]))
                lm = monkeys.setdefault(left, Int(left))
                rm = monkeys.setdefault(right, Int(right))

                s.add(c := tm == operations[op](lm, rm))
                g.add(lm == rm if m[:-1] == "root" else c)

            case [str(m), str(num)]:
                tm = monkeys.setdefault(m[:-1], Int(m[:-1]))

                s.add(c := tm == int(num))
                g.add(c if m[:-1] != "humn" else True)

    assert s.check() == sat
    m = s.model()
    print(m[monkeys["root"]])

    assert g.check() == sat
    m = g.model()
    print(m[monkeys["humn"]])


if __name__ == "__main__":
    main()
