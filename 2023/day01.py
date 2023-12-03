import re 


numbers = ("one", "two", "three", "four", "five", "six", "seven", "eight", "nine")


def main():
    with open("inputs/day01.txt") as f:
        lines = f.read().splitlines()

    silver, gold = 0, 0

    for line in lines:
        digits = [(i, int(c)) for i, c in enumerate(line) if c.isnumeric()]
        words = [(m.start(), n+1) for (n, s) in enumerate(numbers) for m in re.finditer(s, line)]
        
        silver += digits[0][1] * 10 + digits[-1][1]
        gold += (w := sorted(digits + words))[0][1] * 10 + w[-1][1]

    print(f"{silver=}", f"{gold=}")

        
if __name__ == "__main__":
    main()
