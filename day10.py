from io import StringIO

def main():
    c, r, s = 0, 1, 0
    b = StringIO()

    def cycle():
        nonlocal c, r, s, b
        c += 1
        s += c * r * ((c - 20) % 40 == 0)
        b.write("#" if abs(c % 40 - 1 - r) <= 1 else " ")
        b.write("\n" if c % 40 == 0 else "")
        
    with open("inputs/day10.txt") as f:
        for line in f:
            match line.strip().split():
                case ["noop"]:
                    cycle()
                case ["addx", str(n)]:
                    cycle()
                    cycle()
                    r += int(n)

    print(s)
    print(b.getvalue())


if __name__ == "__main__":
    main()
