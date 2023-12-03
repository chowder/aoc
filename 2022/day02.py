from enum import Enum


def score(c1, c2):
    # Draws
    if c1 == c2:
        return c1 + 4
    # Wins
    if (c2 - 1) % 3 == c1:
        return c2 + 7
    # Losses
    else:
        return c2 + 1


def main():
    with open("inputs/day02.txt") as f:
        games = [line.strip().split() for line in f.readlines()]

    silver = [(ord(c1) - ord("A"), ord(c2) - ord("X")) for c1, c2 in games]
    gold = [(c1, ((c1 + c2) - 1) % 3) for c1, c2 in silver]

    for g in (silver, gold):
        print(sum([score(c1, c2) for c1, c2 in g]))


if __name__ == "__main__":
    main()
