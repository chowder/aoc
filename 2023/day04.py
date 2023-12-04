def main():
    with open("inputs/day04.txt") as f:
        lines = f.read().splitlines()

    silver = 0
    gold = 0

    extras = [0] * 10

    for line in lines:
        winning, numbers = line.split(":")[1].split("|")
        winning = set([n for n in winning.split() if n])

        wins = len([n for n in numbers.split() if n and n in winning])

        cards = 1 + extras[0]
        extras = extras[1:] + [0]

        for i in range(wins):
            extras[i] += cards

        silver += 2 ** (wins - 1) if wins else 0
        gold += cards

    print(silver, gold)


if __name__ == "__main__":
    main()
