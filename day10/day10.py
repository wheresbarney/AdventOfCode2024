# https://adventofcode.com/2024/day/10


def q1(lines):
    topo = [[int(x) for x in line] for line in lines]
    trailheadScores = 0
    for y in range(len(topo)):
        for x in range(len(topo[y])):
            trailheadScores += trailheadScore(topo, x, y, 0, 9, set())
    return trailheadScores


def q2(lines):
    topo = [[int(x) for x in line] for line in lines]
    trailheadScores = 0
    for y in range(len(topo)):
        for x in range(len(topo[y])):
            trailheadScores += trailheadScore(topo, x, y, 0, 9, None)
    return trailheadScores


def trailheadScore(topo, x, y, start, end, uniqueDests):
    if x < 0 or y < 0 or x >= len(topo[0]) or y >= len(topo):
        return 0
    if topo[y][x] != start:
        return 0
    if topo[y][x] == end:
        if uniqueDests != None:
            if (x, y) in uniqueDests:
                return 0
            uniqueDests.add((x, y))
        return 1

    return sum(
        [
            trailheadScore(topo, x + dx, y + dy, start + 1, end, uniqueDests)
            for dx, dy in [
                (0, 1),
                (0, -1),
                (1, 0),
                (-1, 0),
            ]
        ]
    )
