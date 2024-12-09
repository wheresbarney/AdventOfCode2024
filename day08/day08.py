# https://adventofcode.com/2024/day/8


from itertools import combinations
from re import T


def q1(lines):
    antennae = {}
    for y in range(len(lines)):
        for x in range(len(lines[y])):
            frequency = lines[y][x]
            if frequency in ".#":
                continue
            if frequency not in antennae:
                antennae[frequency] = [(x, y)]
            else:
                antennae[frequency].append((x, y))

    antinodes = set()
    for frequency, nodes in antennae.items():
        for (x1, y1), (x2, y2) in combinations(nodes, 2):
            anx1 = x1 - (x2 - x1)
            anx2 = x2 + (x2 - x1)
            any1 = y1 - (y2 - y1)
            any2 = y2 + (y2 - y1)

            # print(
            #     f"{frequency} {[(x1, y1), (x2, y2)]} considering {(anx1,any1)}, {(anx2,any2)}"
            # )

            if anx1 >= 0 and anx1 < len(lines[0]) and any1 >= 0 and any1 < len(lines):
                # print(
                #     f"{frequency} {[(x1, y1), (x2, y2)]}: adding antinode1 {(anx1,any1)}"
                # )
                antinodes.add((anx1, any1))
            if anx2 >= 0 and anx2 < len(lines[0]) and any2 >= 0 and any2 < len(lines):
                # print(
                #     f"{frequency} {[(x1, y1), (x2, y2)]}: adding antinode2 {(anx2,any2)}"
                # )
                antinodes.add((anx2, any2))

    return len(antinodes)


def q2(lines):
    antennae = {}
    for y in range(len(lines)):
        for x in range(len(lines[y])):
            frequency = lines[y][x]
            if frequency in ".#":
                continue
            if frequency not in antennae:
                antennae[frequency] = [(x, y)]
            else:
                antennae[frequency].append((x, y))

    antinodes = set()
    for frequency, nodes in antennae.items():
        for (x1, y1), (x2, y2) in combinations(nodes, 2):
            for i in range(len(lines)):
                bust = True

                anx1 = x1 - i * (x2 - x1)
                anx2 = x2 + i * (x2 - x1)
                any1 = y1 - i * (y2 - y1)
                any2 = y2 + i * (y2 - y1)

                # print(
                #     f"{frequency} {[(x1, y1), (x2, y2)]} considering {(anx1,any1)}, {(anx2,any2)}"
                # )

                if (
                    anx1 >= 0
                    and anx1 < len(lines[0])
                    and any1 >= 0
                    and any1 < len(lines)
                ):
                    # print(
                    #     f"{frequency} {[(x1, y1), (x2, y2)]}: adding antinode1 {(anx1,any1)}"
                    # )
                    bust = False
                    antinodes.add((anx1, any1))
                if (
                    anx2 >= 0
                    and anx2 < len(lines[0])
                    and any2 >= 0
                    and any2 < len(lines)
                ):
                    # print(
                    #     f"{frequency} {[(x1, y1), (x2, y2)]}: adding antinode2 {(anx2,any2)}"
                    # )
                    bust = False
                    antinodes.add((anx2, any2))

                if bust:
                    break

    return len(antinodes)
