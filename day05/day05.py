# https://adventofcode.com/2024/day/5

from functools import cmp_to_key

def q1(lines):
    orderings = [list(map(int, l.split("|"))) for l in lines if "|" in l]
    sections = [list(map(int, l.split(","))) for l in lines if "," in l]

    sum_middles = 0
    for s in sections:
        if is_ordered(s, orderings):
            # print(f"{s} is ordered, middle is {s[int(len(s)/2)]}")
            sum_middles += s[int(len(s)/2)]
    return sum_middles


def is_ordered(pages, orderings):
    for lo, hi in orderings:
        try:
            if pages.index(lo) > pages.index(hi):
                # print(f'{pages} disordered: {lo} > {hi}')
                return False
        except ValueError:
            continue
    return True


def q2(lines):
    orderings = [list(tuple(map(int, l.split("|")))) for l in lines if "|" in l]
    sections = [list(map(int, l.split(","))) for l in lines if "," in l]

    sum_middles = 0
    for s in sections:
        if is_ordered(s, orderings):
            continue
        o = sorted(s, key=cmp_to_key(lambda l, r: 1 if [r, l] in orderings else -1))
        # print(f"{s} => {o}, middle is {o[int(len(o)/2)]}")
        sum_middles += o[int(len(o)/2)]
    return sum_middles
