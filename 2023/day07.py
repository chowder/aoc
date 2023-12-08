from collections import defaultdict


def to_score(hand: str) -> tuple:
    count = defaultdict(int)
    for card in hand:
        count[card] += 1

    hand = (hand
            .replace("T", "a")
            .replace("Q", "c")
            .replace("K", "d")
            .replace("A", "e")
            )

    silver = tuple(sorted(count.values(), reverse=True)), hand.replace("J", "b")

    jokers = count.pop("J", 0)
    score = sorted(count.values(), reverse=True)

    gold = (score[0] + jokers, *score[1:]) if score else (jokers,), hand.replace("J", "1")
    return silver, gold


def main():
    with open("inputs/day07.txt") as f:
        lines = f.read().splitlines()

    silver = []
    gold = []
    for line in lines:
        hand, bid = line.split(" ")
        silver_score, gold_score = to_score(hand)

        silver.append((silver_score, int(bid)))
        gold.append((gold_score, int(bid)))

    for p in (silver, gold):
        print(sum((rank + 1) * h[1] for rank, h in enumerate(sorted(p))))


if __name__ == "__main__":
    main()
