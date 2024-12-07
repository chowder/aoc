import os
from concurrent.futures import as_completed
from concurrent.futures.thread import ThreadPoolExecutor


def main():
    with open("inputs/day07.txt") as f:
        equations = f.read().splitlines()

    equations = (e.split(": ") for e in equations)
    equations = [(int(l), list(map(int, r.split(" ")))) for l, r in equations]

    # cpu go brrr
    with ThreadPoolExecutor(max_workers=len(os.sched_getaffinity(0))) as executor:
        def solvable(total, nums, with_concat):
            return total if any(s == total for s in solutions(nums, with_concat, total)) else 0

        for with_concat in (False, True):
            futures = [
                executor.submit(solvable, total, nums, with_concat)
                for total, nums in equations
            ]
            print(sum(future.result() for future in as_completed(futures)))


def solutions(nums, with_concat=False, upper_bound=None):
    if len(nums) == 1:
        yield nums[0]
        return

    if upper_bound and nums[0] > upper_bound:
        return

    yield from solutions([nums[0] + nums[1], *nums[2:]], with_concat, upper_bound)
    yield from solutions([nums[0] * nums[1], *nums[2:]], with_concat, upper_bound)
    if with_concat:
        yield from solutions([int(f"{nums[0]}{nums[1]}"), *nums[2:]], with_concat, upper_bound)


if __name__ == "__main__":
    main()
