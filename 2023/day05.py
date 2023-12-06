import sys


def propagate(seed_start, seed_end, mapping) -> list[tuple]:
    new_ranges = []
    for src_start, src_end, dst in mapping:
        # left outer range
        if seed_start < src_start <= seed_end:
            new_ranges.extend(propagate(seed_start, src_start - 1, mapping))
        # mapped region
        if not (seed_end < src_start or src_end < seed_start):
            overlap = max(seed_start, src_start), min(seed_end, src_end)
            new_ranges.append((dst + (overlap[0] - src_start), dst + (overlap[1] - src_start)))
        # right outer range
        if seed_start <= src_end < seed_end:
            new_ranges.extend(propagate(src_end + 1, seed_end, mapping))

    return new_ranges or [(seed_start, seed_end)]


def main():
    with open("inputs/day05.txt") as f:
        lines = [l for l in f.read().splitlines() if l]

    seeds = [int(s) for s in lines[0].split(": ")[1].split(" ")]

    # Parsing
    maps = []
    current_map = []
    for line in lines[2:]:
        if line.endswith("map:"):
            maps.append(current_map)
            current_map = []
        else:
            dst, src, width = [int(i) for i in line.split(" ")]
            current_map.append([src, src + width - 1, dst])

    maps.append(current_map)

    # Silver
    silver = sys.maxsize
    for seed in seeds:
        current = seed
        for mapping in maps:
            for src_start, src_end, dst in mapping:
                if src_start <= current <= src_end:
                    current = dst + (current - src_start)
                    break
        silver = min(silver, current)

    print(silver)

    # Gold
    gold = sys.maxsize
    for seed, width in zip(seeds[0::2], seeds[1::2]):
        ranges = [(seed, seed + width - 1)]
        for m in maps:
            new_ranges = []
            for seed_start, seed_end in ranges:
                result = propagate(seed_start, seed_end, m)
                new_ranges.extend(result)

            ranges = new_ranges

        gold = min(gold, sorted(ranges)[0][0])

    print(gold)


if __name__ == "__main__":
    main()
