import re


def main():
    with open("inputs/day03.txt") as f:
        memory = f.read().strip()

    e = s = g = 0
    p = re.compile(r"mul\((\d+),(\d+)\)|(do|don't)\(\)")

    for m in p.findall(memory):
        match m:
            case *_, "do": e = 1
            case *_, "don't": e = 0
            case x, y, _:
                s += (t := int(x) * int(y))
                g += e and t

    print(s, g)


if __name__ == "__main__":
    main()
