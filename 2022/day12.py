from collections import deque

DIRS = (0, 1), (1, 0), (0, -1), (-1, 0)

def can_move(a, b, reverse):
    if reverse: 
        a, b = b, a        
    if ord(b) - ord(a) <= 1 and b != "E":
        return True
    return (a, b) in (("S", "a"), ("S", "b"), ("y", "E"), ("z", "E"))


def solve(hm, start, goal, reverse):
    q = deque([(0, start)])
    seen = set([start])
    while q:
        d, (x, y) = q.popleft()
        if (e := hm[y][x]) == goal:
            return d

        for dx, dy in DIRS:
            nx, ny = (x + dx, y + dy)
            if (n := (nx, ny)) in seen:
                continue
                
            if 0 <= nx < len(hm[0]) and 0 <= ny < len(hm) and can_move(e, hm[ny][nx], reverse):
                q.append((d + 1, n))
                seen.add(n)


def main():
    with open("inputs/day12.txt") as f:
        hm = f.read().splitlines()

    for y, line in enumerate(hm):
        for x, c in enumerate(line):
            if c == "S":
                S = (x, y)
            elif c == "E":
                E = (x, y)

    print(solve(hm, S, "E", False))
    print(solve(hm, E, "a", True))

if __name__ == "__main__":
    main()
