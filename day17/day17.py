# https://adventofcode.com/2024/day/17

from sys import argv

DEBUG = len(argv) > 4 and "debug" in argv[4].lower()
print_debug = print if DEBUG else lambda *a, **k: None


def q1(lines):
    a, b, c = [
        int(line.split(":")[1].strip()) for line in lines if line.startswith("Register")
    ]
    program = list(map(int, lines[-1].split(":")[1].strip().split(",")))
    out = run(program, a, b, c)
    return ",".join(map(str, out))


# with a LOT of help from https://github.com/Praful/advent_of_code/blob/main/2024/src/day17.py
def q2(lines):
    a, b, c = [
        int(line.split(":")[1].strip()) for line in lines if line.startswith("Register")
    ]
    return solve(list(map(int, lines[-1].split(":")[1].strip().split(","))), 0, 1)


def solve(program, a, compare_index, possible=set()):
    for n in range(8):
        a2 = (a << 3) | n
        output = run(program, a2, 0, 0)
        if output == program[-compare_index:]:
            if output == program:
                possible.add(a2)
            else:
                solve(program, a2, compare_index + 1, possible)

    if len(possible) > 0:
        return min(possible)
    else:
        return None


def run(program, a, b, c):
    ptr = 0
    out = []

    def combo(operand):
        match operand:
            case 0 | 1 | 2 | 3:
                return operand
            case 4:
                return a
            case 5:
                return b
            case 6:
                return c
            case _:
                raise ValueError(f"Invalid operand {operand}")

    while ptr < len(program):
        opcode = program[ptr]
        operand = program[ptr + 1]
        print_debug(f"{ptr=} {opcode=}, {operand=}, {a=}, {b=}, {c=} {out=}")

        match opcode:
            case 0:  # ADV
                a = a >> combo(operand)
            case 1:  # BXL
                b = b ^ operand
            case 2:  # BST
                b = combo(operand) % 8
            case 3:  # JNZ
                pass
            case 4:  # BXC
                b = b ^ c
            case 5:  # OUT
                out.append(combo(operand) % 8)
            case 6:  # BDV
                b = a >> combo(operand)
            case 7:  # CDV
                c = a >> combo(operand)
            case _:
                raise ValueError(f"Invalid opcode {opcode}")

        if opcode == 3 and a != 0:
            ptr = operand
        else:
            ptr += 2

    return out
