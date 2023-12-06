import math


def ways(t, d):
    hi = (t + math.sqrt((t ** 2) - 4 * d)) / 2
    lo = (t - math.sqrt((t ** 2) - 4 * d)) / 2

    hi = int(math.ceil(hi - 1))
    lo = int(lo + 1)

    return (hi - lo) + 1


def main():
    with open("inputs/day06.txt") as f:
        lines = f.read().splitlines()

    times = [int(t) for t in lines[0].split(":")[1].split(" ") if t]
    distances = [int(d) for d in lines[1].split(":")[1].split(" ") if d]

    # Silver
    silver = 1
    for t, d in zip(times, distances):
        silver *= ways(t, d)

    print(silver)

    # Gold
    time = int(lines[0].split(":")[1].replace(" ", ""))
    distance = int(lines[1].split(":")[1].replace(" ", ""))

    print(ways(time, distance))


if __name__ == "__main__":
    main()
"""
# t = 7
#
# h <= t
#
# h * (t - h) > d
# - h^2 + ht > d
# - h^2 + ht - d > 0

# -t [+-] sqrt(t^2 - 4(-1)(-d)) / 2 * (-1)
# -t [+-] sqrt(t^2 - 4d) / (-2)

t + sqrt(t^2 - 4d) / 2
t - sqrt(t^2 - 4d) / 2



# t^2 - 2d = 0
# t = sqrt(2d)
"""
