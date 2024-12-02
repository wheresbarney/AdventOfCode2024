# https://adventofcode.com/2024/day/2

from itertools import pairwise


def q1(lines):
    safe_reports = 0
    for line in lines:
        levels = [int(x) for x in line.split()]
        if safe(levels):
            safe_reports += 1

    return safe_reports


def q2(lines):
    safe_reports = 0
    for line in lines:
        levels = [int(x) for x in line.split()]
        if safe(levels):
            safe_reports += 1
        else:
            for i in range(len(levels)):
                damped_levels = levels[:i] + levels[i + 1 :]
                if safe(damped_levels):
                    safe_reports += 1
                    break
    return safe_reports


def safe(levels):
    dir = -1 if levels[0] > levels[1] else 1
    for pair in pairwise(levels):
        gap = dir * (pair[1] - pair[0])
        if gap < 1 or gap > 3:
            return False
    return True
