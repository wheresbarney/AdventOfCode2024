# https://adventofcode.com/2024/day/4


def q1(lines):
    count = 0
    for y in range(len(lines)):
        for x in range(len(lines[0])):
            for dx, dy in [
                (0, 1),
                (0, -1),
                (1, 0),
                (-1, 0),
                (1, 1),
                (1, -1),
                (-1, 1),
                (-1, -1),
            ]:
                if isWord(lines, "XMAS", x, y, dx, dy):
                    count = count + 1
    return count


def isWord(lines, word, x, y, dx, dy):
    if x < 0 or y < 0 or x >= len(lines[0]) or y >= len(lines):
        return False
    if lines[y][x] != word[0]:
        return False
    if len(word) == 1:
        return True
    return isWord(lines, word[1:], x + dx, y + dy, dx, dy)


def q2(lines):
    count = 0
    for y in range(len(lines)):
        for x in range(len(lines[0])):
            if lines[y][x] != "A":
                continue
            localCount = 0
            for dx, dy in ((-1, -1), (1, -1), (1, 1), (-1, 1)):
                if isWord(lines, "MAS", x + dx, y + dy, -dx, -dy):
                    localCount = localCount + 1
            if localCount == 2:
                count = count + 1
    return count
