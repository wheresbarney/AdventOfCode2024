# https://adventofcode.com/2024/day/25


def q1(lines):
    locks = []
    keys = []
    for i in range(len(lines)):
        if lines[i] == "#####" and (i == 0 or lines[i - 1] == ""):
            assert lines[i + 6] == "....."
            lock = []
            for x in range(5):
                pin = 0
                for y in range(i + 5, i, -1):
                    if lines[y][x] == "#":
                        pin = y - i
                        break
                    assert lines[y][x] == "."
                lock.append(pin)
            locks.append(tuple(lock))
        elif lines[i] == "....." and (i == 0 or lines[i - 1] == ""):
            assert lines[i + 6] == "#####"
            key = []
            for x in range(5):
                pin = 0
                for y in range(i + 1, i + 6):
                    if lines[y][x] == "#":
                        pin = 6 - y + i
                        break
                    assert lines[y][x] == "."
                key.append(pin)
            keys.append(tuple(key))

    fits = 0
    for key in keys:
        for lock in locks:
            fit = True
            for pin in range(5):
                if key[pin] + lock[pin] > 5:
                    fit = False
                    break
            if fit:
                fits += 1
    return fits
