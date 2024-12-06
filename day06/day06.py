# https://adventofcode.com/2024/day/6

directions = {"^": (0, -1), "V": (0, 1), "<": (-1, 0), ">": (1, 0)}
turns = {"^": ">", "V": "<", "<": "^", ">": "V"}

def q1(lines):
    x, y, dir = findGuard(lines)
    visited = {(x, y)}

    while True:
        nextx, nexty = x + directions[dir][0], y + directions[dir][1]

        if nextx < 0 or nexty < 0 or nextx >= len(lines[0]) or nexty >= len(lines):
            break

        if lines[nexty][nextx] == "#":
            # don't move there, turn instead
            dir = turns[dir]
            continue

        # print(f"moving {dir} to {nextx}, {nexty}")
        x, y = nextx, nexty
        visited.add((x, y))

    return len(visited)


def findGuard(lines):
    for y in range(len(lines)):
        for x in range(len(lines[y])):
            if lines[y][x] in "^V<>":
                return x, y, lines[y][x]
    return None


def q2(lines):
    loop_count = 0
    for y in range(len(lines)):
        for x in range(len(lines[y])):
            if lines[y][x] == ".":
                if loops(lines, (x, y)):
                    loop_count += 1
    return loop_count


def loops(lines, block):
    x, y, dir = findGuard(lines)
    visited = {(x, y, dir)}

    while True:
        nextx, nexty = x + directions[dir][0], y + directions[dir][1]

        if nextx < 0 or nexty < 0 or nextx >= len(lines[0]) or nexty >= len(lines):
            break

        if lines[nexty][nextx] == "#" or (nextx, nexty) == block:
            # don't move there, turn instead
            dir = turns[dir]
            continue

        if (nextx, nexty, dir) in visited:
            # print(f"loop detected for {block=} at {x},{y} {dir}")
            return True

        x, y = nextx, nexty
        visited.add((x, y, dir))

    return False
