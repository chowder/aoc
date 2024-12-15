import math

MEMO: dict[(int, int), int] = {}


def blink(stone) -> list[int]:
    match stone:
        case 0:
            return [1]
        case n if (d := int(math.log10(n)) + 1) % 2 == 0:
            return list(map(int, divmod(n, 10 ** (d / 2))))
        case n:
            return [n * 2024]


def num_stones(stones: list[int], blinks: int) -> int:
    if blinks == 0:
        return len(stones)

    count = 0
    for stone in stones:
        if (stone, blinks) not in MEMO:
            MEMO[(stone, blinks)] = num_stones(blink(stone), blinks - 1)

        count += MEMO[(stone, blinks)]

    return count


def main():
    with open("inputs/day11.txt") as f:
        stones = list(map(int, f.read().strip().split()))

    print(num_stones(stones, blinks=25))
    print(num_stones(stones, blinks=75))


if __name__ == "__main__":
    main()
