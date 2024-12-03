# https://adventofcode.com/2024/day/3


import re


def q1(input):
    total = 0
    for m in re.finditer(r'mul\((\d{1,3}),(\d{1,3})\)', ''.join(input)):
        total = total + int(m.group(1)) * int(m.group(2))
    return total

def q2(input):
    cleaned = re.sub(r"don't\(\).*?do\(\)", '', ''.join(input))
    return q1(cleaned.splitlines())
