import itertools

Rules = dict[str, set[str]]
Update = list[str]


def ok(update: Update, rules: Rules) -> bool:
    seen = set()
    return not any(rules.get(n, set()) & seen or seen.add(n) for n in update)


def fixup(update: Update, rules: Rules) -> Update:
    fixed = []
    for n in update:
        come_after = rules.get(n, set())
        fixed = [c for c in fixed if c not in come_after] + [n] + [c for c in fixed if c in come_after]

    return fixed


def main():
    with open("inputs/day05.txt") as f:
        lines = f.read().splitlines()

    s = lines.index("")

    pairs = sorted([l.split("|") for l in lines[:s]], key=lambda x: x[0])
    rules: Rules = {key: set(x[1] for x in group) for key, group in itertools.groupby(pairs, key=lambda x: x[0])}
    updates: list[Update] = [l.split(",") for l in lines[s + 1:]]

    silver = gold = 0
    for update in updates:
        if ok(update, rules):
            silver += int(update[len(update) // 2])
        else:
            gold += int((fixed := fixup(update, rules))[len(fixed) // 2])

    print(silver, gold)


if __name__ == "__main__":
    main()
