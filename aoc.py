#!/usr/bin/env python3
# https://adventofcode.com/2024

from sys import argv
from time import perf_counter

# day func input
day = "day" + argv[1]
src = f"./{day}/{day}.py"
function = argv[2]
input = f"./{day}/{argv[3]}.txt"

with open(src, "rb") as f:
    code = compile(f.read(), src, "exec")
exec(code)

with open(input, "r") as file:
    data = [line.rstrip() for line in file]

t1 = perf_counter()
if "1" in function:
    output = q1(data)  # type: ignore
else:
    output = q2(data)  # type: ignore
t2 = perf_counter()

print(output)
print(f"Execution time: {t2 - t1:0.4f} seconds")
