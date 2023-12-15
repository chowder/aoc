import itertools
from functools import cache


def count_load(platform):
    return sum([len(column) - i for column in platform for i, v in enumerate(column) if v == 'O'])


def rotate_platform(p):
    return tuple(''.join(r)[::-1] for r in zip(*p))


@cache
def tilt_segment(s):
    return 'O' * (rocks := s.count('O')) + '.' * (len(s) - rocks)


@cache
def tilt_row(r):
    return "#".join(tilt_segment(s) for s in r.split("#"))


def tilt_platform(p):
    return tuple(tilt_row(r) for r in p)


def cycle_platform(platform):
    for _ in range(4):
        platform = rotate_platform(tilt_platform(platform))
    return platform


def repeats_between(platform):
    seen = {platform: 0}
    for i in itertools.count(start=1):
        platform = cycle_platform(platform)
        if platform in seen:
            return seen[platform], i
        seen[platform] = i


def main():
    with open("inputs/day14.txt") as f:
        platform = f.read().splitlines()

    # start north
    for _ in range(3):
        platform = rotate_platform(platform)

    # silver
    print(count_load(tilt_platform(platform)))

    # gold
    cycle_start, cycle_end = repeats_between(platform)
    repetitions = (1_000_000_000 - cycle_end) % (cycle_end - cycle_start) + cycle_end
    for _ in range(repetitions):
        platform = cycle_platform(platform)

    print(count_load(platform))


if __name__ == "__main__":
    main()
