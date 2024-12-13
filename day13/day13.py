# https://adventofcode.com/2024/day/13


from math import lcm
from re import findall

# ax + bx = px
# ay + by = py
# 94a + 22b = 8400
# 34a + 67b = 5400

# lcm(94, 34) = 1598

# scale up
# 1598a + 374b = 142_800
# 1598a + 3149b = 253_800

# subtract
# -2775b = -111000

# solve for b
# b = -111000 / -2775 = 40

# solve for a
# a = (142_800 - 374b)/1598 = (142_800 - 374*40)/1598 = 80


def q1(lines):
    lines = " ".join(lines)
    a = [(int(x), int(y)) for x, y in findall(r"Button A: X\+(\d+), Y\+(\d+)", lines)]
    b = [(int(x), int(y)) for x, y in findall(r"Button B: X\+(\d+), Y\+(\d+)", lines)]
    p = [(int(x), int(y)) for x, y in findall(r"Prize: X=(\d+), Y=(\d+)", lines)]

    tokens = 0
    for (ax, ay), (bx, by), (px, py) in zip(a, b, p):

        m = lcm(ax, ay)

        cx = m // ax
        ax *= cx
        bx *= cx
        px *= cx

        cy = m // ay
        ay *= cy
        by *= cy
        py *= cy

        assert ax == ay

        b = (px - py) // (bx - by)
        a = (px - bx * b) // ax

        # print(
        #     f"A: X+{ax}, Y+{ay} B: X+{bx}, Y+{by} Prize: X={px} Y={py}=> a={a} b={b} (lcm={m})"
        # )

        if a * ax + b * bx == px and a * ay + b * by == py:
            tokens += 3 * a + b
    return tokens


def q2(lines):
    lines = " ".join(lines)
    a = [(int(x), int(y)) for x, y in findall(r"Button A: X\+(\d+), Y\+(\d+)", lines)]
    b = [(int(x), int(y)) for x, y in findall(r"Button B: X\+(\d+), Y\+(\d+)", lines)]
    p = [
        (int(x) + 10_000_000_000_000, int(y) + 10_000_000_000_000)
        for x, y in findall(r"Prize: X=(\d+), Y=(\d+)", lines)
    ]

    tokens = 0
    for (ax, ay), (bx, by), (px, py) in zip(a, b, p):
        # print(f"A: X+{ax}, Y+{ay} B: X+{bx}, Y+{by} Prize: X={px} Y={py})")

        m = lcm(ax, ay)

        cx = m // ax
        ax *= cx
        bx *= cx
        px *= cx

        cy = m // ay
        ay *= cy
        by *= cy
        py *= cy

        assert ax == ay

        b = (px - py) // (bx - by)
        a = (px - bx * b) // ax

        if a * ax + b * bx == px and a * ay + b * by == py:
            # print(f"  SOLUTION: A={a}, B={b}")
            tokens += 3 * a + b
        # else:
        # print(f"  NO SOLUTION")
    return tokens
