# https://adventofcode.com/2024/day/1


def q1(lines):
    left, right = map(sorted, zip(*(map(int, s.split()) for s in lines)))
    merged = zip(left, right)

    return sum([abs(t[0] - t[1]) for t in merged])


def q2(lines):
    left, right = zip(*(map(int, s.split()) for s in lines))

    return sum([l * right.count(l) for l in left])
