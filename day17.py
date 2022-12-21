shapes = (
    # -
    ((0, 0), (1, 0), (2, 0), (3, 0)),
    # +
    ((0, 0), (2, 0), (1, 1), (1, -1)),
    # ˩
    ((0, 0), (1, 0), (2, 0), (2, 1), (2, 2)),
    # |
    ((0, 0), (0, 1), (0, 2), (0, 3)),
    # □
    ((0, 0), (1, 0), (1, 1), (0, 1)),
)


def can_move(occupied, rock, rock_type, direction):
    for dx, dy in shapes[rock_type]:
        x, y = rock[0] + dx + direction[0], rock[1] + dy + direction[1]
        if (x, y) in occupied or x > 6 or x < 0 or y < 1:
            return False
    return True


def fingerprint(occupied, highest, size=5):
    return hash("".join("#" if (x, y) in occupied else "." for y in range(highest, highest - size, -1) for x in range(7)))


def main():
    with open("inputs/day17.txt") as f:
        jets = f.read().strip()

    for target in (2022, 1000000000000):
        # so much state!!!
        highest, rocks, step = 0, 0, 0
        rock = (2, 4)
        rock_type = 0
        occupied = set()
        fingerprints = {}
        cycle_found = False
        extra_height = 0

        while rocks < target:
            direction = (-1, 0) if jets[step % len(jets)] == "<" else (1, 0)

            if can_move(occupied, rock, rock_type, direction):
                rock = rock[0] + direction[0], rock[1] + direction[1]

            if can_move(occupied, rock, rock_type, (0, -1)):
                rock = rock[0], rock[1] - 1
            else:
                pieces = [(rock[0] + dx, rock[1] + dy) for dx, dy in shapes[rock_type]]
                occupied.update(pieces)
                highest = max(highest, max(y for _, y in pieces))
                rock_type = (rock_type + 1) % len(shapes)
                rock = (2, highest + 4 + (rock_type == 1))
                rocks += 1

                if not cycle_found:
                    if (key := ((step + 1) % len(jets), rock_type, fingerprint(occupied, highest))) in fingerprints:
                        previous_highest, previous_rocks = fingerprints[key]
                        extra_cycles = (target - rocks) // (rocks_per_cycle := rocks - previous_rocks)
                        extra_height = extra_cycles * (highest - previous_highest)
                        rocks += extra_cycles * rocks_per_cycle
                        cycle_found = True
                    else:
                        fingerprints[key] = (highest, rocks)

            step += 1

        print(highest + extra_height)


if __name__ == "__main__":
    main()
