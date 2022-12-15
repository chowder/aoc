import re


def merge_intervals(intervals):
    merged = []
    for interval in sorted(intervals):
        if not merged or merged[-1][1] < interval[0]:
            merged.append(interval)
        else:
            merged[-1][1] = max(merged[-1][1], interval[1])
    return merged


def get_intervals(lines, row):
    intervals = []
    for s, b in lines:
        radius = abs(s[0] - b[0]) + abs(s[1] - b[1])
        distance = abs(row - s[1])
        if (width := radius - distance) > 0:
            intervals.append([s[0] - width, s[0] + width])

    return merge_intervals(intervals)


def main():
    with open("inputs/day15.txt") as f:
        lines = [re.findall(r"x=(-?\d*), y=(-?\d*)", line) for line in f]
        lines = [((int(s[0]), int(s[1])), (int(b[0]), int(b[1]))) for s, b in lines]

    occupied = sum(i[1] - i[0] for i in merge_intervals(get_intervals(lines, 2000000)))
    print(occupied)

    for i in range(4000000):
        if len((intervals := get_intervals(lines, i))) > 1:
            print((intervals[0][1] + 1) * 4000000 + i)
            break


if __name__ == "__main__":
    main()
