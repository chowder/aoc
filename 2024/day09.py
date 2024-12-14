from collections import deque
from itertools import zip_longest


def compact_blocks(blocks, spaces):
    blocks, spaces = deque(enumerate(blocks)), deque(spaces)
    result = []

    while spaces and blocks:
        fid, size = blocks.popleft()
        result.append((fid, size))
        space = spaces.popleft()

        while space and blocks:
            fid, size = blocks.pop()
            if size > space:
                result.append((fid, space))
                blocks.append((fid, size - space))
                break
            else:
                result.append((fid, size))
                space -= size

    pos = checksum = 0
    for fid, size in result:
        for i in range(size):
            checksum += (pos * fid)
            pos += 1

    return checksum


def compact_files(blocks, spaces):
    pos = 0
    files = []
    for fid, (size, space) in enumerate(zip_longest(blocks, spaces, fillvalue=0)):
        files.append((pos, fid, size))
        pos += (size + space)

    ptr = len(files) - 1
    moved = set()

    while ptr > 0:
        rpos, rfid, rsize = files[ptr]

        if rfid in moved:
            ptr -= 1
            continue

        for left in range(ptr):
            (l1pos, _, l1size), (l2pos, _, _) = files[left], files[left + 1]
            gap = l2pos - (l1pos + l1size)

            if gap == 0:
                continue

            if gap >= rsize:
                del files[ptr]
                files.insert(left + 1, (l1pos + l1size, rfid, rsize))
                moved.add(rfid)
                break
        else:
            ptr -= 1

    checksum = 0
    for pos, fid, size in files:
        for i in range(size):
            checksum += (pos + i) * fid

    return checksum


def main():
    with open("inputs/day09.txt") as f:
        disk = f.read().strip()

    blocks, spaces = [list(map(int, c)) for c in (disk[0::2], disk[1::2])]

    result = compact_blocks(blocks, spaces)
    print(result)

    result = compact_files(blocks, spaces)
    print(result)


if __name__ == "__main__":
    main()
