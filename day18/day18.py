# https://adventofcode.com/2024/day/18

from heapq import heappop, heappush


def q1(lines):
    grid, count = (7, 12) if len(lines) == 25 else (71, 1024)
    corrupted = [tuple(map(int, l.split(","))) for l in lines[:count]]
    return dijsktra(grid, corrupted)


def q2(lines):
    grid = 7 if len(lines) == 25 else 71
    corrupted = [tuple(map(int, l.split(","))) for l in lines]
    lo = 0
    hi = len(lines) - 1
    while lo + 1 != hi:
        next = lo + (hi - lo) // 2
        path = dijsktra(grid, corrupted[:next])
        # print(f"{lo=}, {hi=} => {next}: {path}")
        if path is None:
            hi = next
        else:
            lo = next
    return corrupted[lo]


def dijsktra(grid, corrupted):
    work = [(0, ((0, 0),))]
    best = {}
    while work:
        cost, path = heappop(work)
        x, y = path[-1]

        if x == y == grid - 1:
            return cost

        for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            nx, ny = next = x + dx, y + dy
            if (
                0 <= nx < grid
                and 0 <= ny < grid
                and next not in corrupted
                and best.get(next, cost + 2) > cost + 1
            ):
                best[next] = cost + 1
                heappush(work, (cost + 1, path + (next,)))
    return None
