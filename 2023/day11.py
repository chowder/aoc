from itertools import combinations


def main():
    with open("inputs/day11.txt") as f:
        image = f.read().splitlines()

    galaxies = [(r, c) for r, line in enumerate(image) for c, l in enumerate(line) if l == "#"]

    empty_rows = set(i for i in range(len(image)) if not any(i == r for r, _ in galaxies))
    empty_columns = set(i for i in range(len(image[0])) if not any(i == c for _, c in galaxies))

    def get_distance(from_galaxy, to_galaxy, expansion) -> int:
        from_row, from_column = from_galaxy
        to_row, to_column = to_galaxy
        distance = abs(from_row - to_row) + abs(from_column - to_column)

        bottom, top = (from_row, to_row) if from_row > to_row else (to_row, from_row)
        distance += len([r for r in empty_rows if top < r < bottom]) * expansion

        left, right = (from_column, to_column) if from_column < to_column else (to_column, from_column)
        distance += len([c for c in empty_columns if left < c < right]) * expansion

        return distance

    silver = sum([get_distance(from_, to, 1) for from_, to in combinations(galaxies, 2)])
    gold = sum([get_distance(from_, to, 1000000 - 1) for from_, to in combinations(galaxies, 2)])

    print(silver, gold)


if __name__ == "__main__":
    main()
