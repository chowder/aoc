from collections import defaultdict


def main():
    with open("inputs/day07.txt") as f:
        cwd = []
        dirs = defaultdict(int)
        for line in f:
            match line.strip().split():
                case ["$", "cd", ".."]:
                    cwd.pop()
                case ["$", "cd", str(path)]:
                    cwd.append(path)
                case [str(size), str(name)] if size.isnumeric():
                    for i in range(len(cwd)):
                        dirs[tuple(cwd[:i + 1])] += int(size)

        print(sum(filter(lambda d: d <= 100000, dirs.values())))
        print(min(filter(lambda d: d >= dirs[("/",)] - 40000000, dirs.values())))


if __name__ == "__main__":
    main()
