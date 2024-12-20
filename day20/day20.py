# https://adventofcode.com/2024/day/20


from heapq import heappop, heappush
from collections import defaultdict


def q1(lines):
    path = dijsktra(lines)
    distMap = {path[i]: i for i in range(len(path))}
    shortcutDeltas = frozenset(
        (
            (0, 2),
            (0, -2),
            (2, 0),
            (-2, 0),
            (1, 1),
            (-1, -1),
            (1, -1),
            (-1, 1),
        )
    )
    savings = defaultdict(int)
    for i in range(len(path)):
        point = path[i]
        for dx, dy in shortcutDeltas:
            shortcut = (point[0] + dx, point[1] + dy)
            if shortcut in distMap and distMap[shortcut] - i > 2:
                savings[distMap[shortcut] - i - 2] += 1

    return sum(v for k, v in savings.items() if k >= 100)


def q2(lines):
    path = dijsktra(lines)

    minSaving = 50 if len(lines) == 15 else 100
    savings = defaultdict(int)

    for i in range(len(path)):
        for j in range(i + minSaving, len(path)):
            shortcutTime = abs(path[i][0] - path[j][0]) + abs(path[i][1] - path[j][1])
            if shortcutTime <= 20:
                savings[j - i - shortcutTime] += 1

    if minSaving == 50:
        return sorted(savings.items())
    return sum(v for k, v in savings.items() if k >= minSaving)


def dijsktra(grid):
    y = [y for y in range(len(grid)) if "S" in grid[y]][0]
    start = [(x, y) for x in range(len(grid[y])) if grid[y][x] == "S"][0]
    work = [(0, (start,))]
    best = {}
    while work:
        cost, path = heappop(work)
        x, y = path[-1]

        if grid[y][x] == "E":
            return path

        for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            nx, ny = next = x + dx, y + dy
            if (
                0 <= nx < len(grid[0])
                and 0 <= ny < len(grid)
                and grid[y][x] != "#"
                and best.get(next, cost + 2) > cost + 1
            ):
                best[next] = cost + 1
                heappush(work, (cost + 1, path + (next,)))
    return ()
