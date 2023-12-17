def to_digit(s: str) -> int:
    if s == "-":
        return -1
    if s == "=":
        return -2
    return int(s)


snafu = ["0", "1", "2", "=", "-"]


def snafu_add(left: str, right: str) -> str:
    carry = 0
    result = ""

    for l, r in zip(reversed(left), reversed(right)):
        l, r = to_digit(l), to_digit(r)
        c = l + r + carry
        if c >= 3:
            carry = 1
            c -= 5
        elif c <= -3:
            carry = -1
            c += 5
        else:
            carry = 0

        result += snafu[c]

    return result[::-1]


def main():
    with open("inputs/day25.txt") as f:
        lines = f.read().splitlines()

    width = 50  # i am lazy
    lines = [l.zfill(width) for l in lines]

    total = "0" * width
    for line in lines:
        total = snafu_add(total, line)

    print(total)


if __name__ == "__main__":
    main()
