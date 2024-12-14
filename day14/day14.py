# https://adventofcode.com/2024/day/14


from dataclasses import dataclass
from math import prod
from re import findall


@dataclass
class Robot:
    pos_x: int
    pos_y: int
    vel_x: int
    vel_y: int


def q1(lines):
    robots = [
        Robot(int(px), int(py), int(vx), int(vy))
        for px, py, vx, vy in findall(
            r"p=(-?\d+),(-?\d+) v=(-?\d+),(-?\d+)", " ".join(lines)
        )
    ]

    moves = 100
    if len(robots) == 12:
        floor_x = 11
        floor_y = 7
    else:
        floor_x = 101
        floor_y = 103

    coords = run(robots, moves, floor_x, floor_y)

    quadrants = [0] * 4
    for x, y in coords:
        if x < floor_x // 2:
            if y < floor_y // 2:
                quadrants[0] += 1
            elif y > floor_y // 2:
                quadrants[1] += 1
        elif x > floor_x // 2:
            if y < floor_y // 2:
                quadrants[2] += 1
            elif y > floor_y // 2:
                quadrants[3] += 1

    return prod(quadrants)


def run(robots, moves, floor_x, floor_y):
    return [
        ((r.pos_x + r.vel_x * moves) % floor_x, (r.pos_y + r.vel_y * moves) % floor_y)
        for r in robots
    ]


def q2(lines):
    robots = [
        Robot(int(px), int(py), int(vx), int(vy))
        for px, py, vx, vy in findall(
            r"p=(-?\d+),(-?\d+) v=(-?\d+),(-?\d+)", " ".join(lines)
        )
    ]

    if len(robots) == 12:
        floor_x = 11
        floor_y = 7
    else:
        floor_x = 101
        floor_y = 103

    elapsed = 0
    while True:
        elapsed += 1
        coords = set(run(robots, elapsed, floor_x, floor_y))
        if elapsed % 10_000 == 0:
            print(f"{elapsed=}")

        for x, y in coords:
            if all(map(lambda i: (x + i, y) in coords, range(1, 12))):
                print(f"tree found at {elapsed}")
                for y in range(floor_y):
                    print(
                        "".join(
                            ["#" if (x, y) in coords else " " for x in range(floor_x)]
                        )
                    )
                break
