# https://adventofcode.com/2024/day/21


from functools import lru_cache, cache


def q1(codes):
    testComplexity = 0
    for code in codes:
        input = directional(directional(numeric(code)))
        assert testNumeric(testDirectional(testDirectional(input))) == code
        testComplexity += int(code[:3]) * len(input)

    complexity = solve(codes, 2)
    assert testComplexity == complexity, f"{testComplexity} != {complexity}"

    return complexity


def q2(codes):
    return solve(codes, 25)


def solve(codes, loops):
    return sum(int(code[:3]) * solve2(code, loops) for code in codes)


DIRECTIONAL_BUTTONS = {"^": (1, 0), "A": (2, 0), "<": (0, 1), "v": (1, 1), ">": (2, 1)}
NUMERIC_BUTTONS = {
    "A": (2, 3),
    "0": (1, 3),
    "1": (0, 2),
    "2": (1, 2),
    "3": (2, 2),
    "4": (0, 1),
    "5": (1, 1),
    "6": (2, 1),
    "7": (0, 0),
    "8": (1, 0),
    "9": (2, 0),
}


def numeric(code):
    out = []
    current = NUMERIC_BUTTONS["A"]

    for c in code:
        next = NUMERIC_BUTTONS[c]

        if (next[1] == 3 and current[0] == 0) or (next[0] == 0 and current[1] == 3):
            # always do rights before downs, ups before lefts, then we avoid the blank space
            out += [">"] * max(0, next[0] - current[0])
            out += ["v"] * max(0, next[1] - current[1])
            out += ["^"] * max(0, current[1] - next[1])
            out += ["<"] * max(0, current[0] - next[0])
        else:
            # no danger of hitting the blank space, optimise
            out += ["v"] * max(0, next[1] - current[1])
            out += [">"] * max(0, next[0] - current[0])
            out += ["<"] * max(0, current[0] - next[0])
            out += ["^"] * max(0, current[1] - next[1])
        out.append("A")
        current = next
    return "".join(out)


def directional(code):
    out = []
    current = DIRECTIONAL_BUTTONS["A"]

    for c in code:
        next = DIRECTIONAL_BUTTONS[c]
        out.append(nextDirectional(current, next))
        current = next
    return "".join(out)


def nextDirectional(current, next):
    out = []
    # always do downs before lefts, rights before ups, then we avoid the blank space
    out += [">"] * max(0, next[0] - current[0])
    out += ["^"] * max(0, current[1] - next[1])
    out += ["v"] * max(0, next[1] - current[1])
    out += ["<"] * max(0, current[0] - next[0])
    out.append("A")

    return "".join(out)


@lru_cache
def sequenceLength(s, loops):
    if loops == 0:
        return len(s)
    chunks = [chunk + "A" for chunk in directional(s).split("A")[:-1]]
    return sum(sequenceLength(chunk, loops - 1) for chunk in chunks)


def testDirectional(code):
    out = []
    current = list(DIRECTIONAL_BUTTONS["A"])
    reverseMap = dict(zip(DIRECTIONAL_BUTTONS.values(), DIRECTIONAL_BUTTONS.keys()))
    for c in code:
        match c:
            case "A":
                out.append(reverseMap[tuple(current)])
            case ">":
                current[0] += 1
            case "<":
                current[0] -= 1
            case "v":
                current[1] += 1
            case "^":
                current[1] -= 1
        assert current != [0, 0]
    return "".join(out)


def testNumeric(code):
    out = []
    current = list(NUMERIC_BUTTONS["A"])

    reverseMap = dict(zip(NUMERIC_BUTTONS.values(), NUMERIC_BUTTONS.keys()))
    for c in code:
        match c:
            case "A":
                out.append(reverseMap[tuple(current)])
            case ">":
                current[0] += 1
            case "<":
                current[0] -= 1
            case "v":
                current[1] += 1
            case "^":
                current[1] -= 1
        assert current != [0, 3]
    return "".join(out)


# this solution from:
# https://www.reddit.com/r/adventofcode/comments/1hj2odw/comment/m3482ai/?utm_source=share&utm_medium=web3x&utm_name=web3xcss&utm_term=1&utm_content=share_button

num = ["789", "456", "123", " 0A"]
dir = [" ^A", "<v>"]


def path(pad, fr, to):
    fx, fy = next((x, y) for y, r in enumerate(pad) for x, c in enumerate(r) if c == fr)
    tx, ty = next((x, y) for y, r in enumerate(pad) for x, c in enumerate(r) if c == to)

    def g(x, y, s):
        if (x, y) == (tx, ty):
            yield s + "A"
        if tx < x and pad[y][x - 1] != " ":
            yield from g(x - 1, y, s + "<")
        if ty < y and pad[y - 1][x] != " ":
            yield from g(x, y - 1, s + "^")
        if ty > y and pad[y + 1][x] != " ":
            yield from g(x, y + 1, s + "v")
        if tx > x and pad[y][x + 1] != " ":
            yield from g(x + 1, y, s + ">")

    return min(g(fx, fy, ""), key=lambda p: sum(a != b for a, b in zip(p, p[1:])))


@cache
def solve2(seq, maxLoops, loops=0):
    if loops > maxLoops:
        return len(seq)
    return sum(
        solve2(path(dir if loops else num, fr, to), maxLoops, loops + 1)
        for fr, to in zip("A" + seq, seq)
    )
