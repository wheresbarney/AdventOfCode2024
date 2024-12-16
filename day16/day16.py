# https://adventofcode.com/2024/day/16

from heapq import heappop, heappush

def q1(lines):
    graph, start, end, _ = build_graph(lines)

    q = [(0,start,())]
    seen = set()
    mins = {start: 0}

    while q:
        (cost, current, path) = heappop(q)
        if current in seen:
            continue
        seen.add(current)

        if current in end:
            return cost

        path = (current, path)
        for next, weight in graph[current].items():
            if next in seen:
                continue
            prevCost = mins.get(next, None)
            thisCost = cost + weight
            if prevCost is None or thisCost < prevCost:
                mins[next] = thisCost
                heappush(q, (thisCost, next, path))


def q2(lines):
    graph, start, end, walls = build_graph(lines)

    q = [(0,start,{(start[0],start[1]),})]
    # seen = set()
    mins = {start: 0}

    best_cost = None
    best_seats = set()

    while q:
        (cost, current, path) = heappop(q)
        # if current in seen:
        #     continue
        # seen.add(current)

        if current in end:
            best_cost = cost
            best_seats |= path
            continue
        elif best_cost is not None and cost > best_cost:
            continue

        for next, weight in graph[current].items():
            # if next in seen:
            #     continue
            prevCost = mins.get(next, None)
            thisCost = cost + weight
            if prevCost is None or thisCost <= prevCost:
                mins[next] = thisCost
                heappush(q, (thisCost, next, path | {(next[0], next[1]),}))

    for y in range(len(lines)):
        row = []
        for x in range(len(lines[y])):
            if (x, y) in best_seats:
                row.append("@")
            elif (x, y) in walls:
                row.append(":")
            else:
                row.append(" ")
        print("".join(row))

    return best_cost, len(best_seats)


def build_graph(lines):
    start = end = None
    walls = set()
    for y in range(len(lines)):
        for x in range(len(lines[y])):
            if lines[y][x] == "#":
                walls.add((x, y))
            if lines[y][x] == "S":
                start = (x, y, "E")
            elif lines[y][x] == "E":
                end = {(x, y, d) for d in "NESW"}
    assert start and end

    graph = {}
    dirs = {"N": (0, -1), "E": (1, 0), "S": (0, 1), "W": (-1, 0)}
    turns = { "N": set("EW"), "E": set("NS"), "S": set("EW"), "W": set("NS"), }
    for y in range(len(lines)):
        for x in range(len(lines[y])):
            if lines[y][x] == "#":
                continue
            for d_curr in "NESW":
                graph[(x, y, d_curr)] = {}
                for d_to in "NESW":
                    if d_to == d_curr:
                        next = (x + dirs[d_to][0], y + dirs[d_to][1])
                        if next not in walls:
                            graph[(x, y, d_curr)][(*next, d_to)] = 1
                    elif d_to in turns[d_curr]:
                        graph[(x, y, d_curr)][(x, y, d_to)] = 1000

    return graph, start, end, walls
