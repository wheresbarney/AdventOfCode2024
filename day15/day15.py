# https://adventofcode.com/2024/day/15

def q1(lines):
    map = [list(line) for line in lines if line.startswith("#")]
    moves = "".join([line for line in lines if line and line[0] in "<>^v"])

    robot = None
    for y in range(len(map)):
        for x in range(len(map[y])):
            if map[y][x] == "@":
                robot = (x, y)

    for move in moves:
        robot, map = doMove(robot, move, map)
        # print(f"moved robot {move} to {robot} V")
        # for line in map:
        #     print("".join(line))

    gps = 0
    for y in range(len(map)):
        for x in range(len(map[y])):
            if map[y][x] == "O":
                gps += 100 * y + x

    return gps


moveMap = {"^": (0, -1), "v": (0, 1), "<": (-1, 0), ">": (1, 0)}


def doMove(piece, move, map):
    x = piece[0] + moveMap[move][0]
    y = piece[1] + moveMap[move][1]

    if map[y][x] == "O":
        _, map = doMove((x, y), move, map)

    if map[y][x] == "#":
        return piece, map

    if map[y][x] == ".":
        map[y][x] = map[piece[1]][piece[0]]
        map[piece[1]][piece[0]] = "."
        piece = (x, y)

    return piece, map


def q2(lines):
    map = [list(line) for line in lines if line.startswith("#")]
    moves = "".join([line for line in lines if line and line[0] in "<>^v"])

    newMap = []
    for mapRow in map:
        newMapRow = []
        for tile in mapRow:
            if tile in "#.":
                newMapRow += [tile] * 2
            elif tile == "O":
                newMapRow += "[]"
            else:
                assert tile == "@"
                newMapRow += "@."
        newMap.append(newMapRow)
    map = newMap

    robot = None
    bounds = set()
    crates = set()
    for y in range(len(map)):
        for x in range(len(map[y])):
            if map[y][x] == "@":
                robot = (x, y)
            elif map[y][x] == "#":
                bounds.add((x, y))
            elif map[y][x] == "[":
                crates.add((x, y))

    for move in moves:
        robot = doWideMove(robot, move, crates, bounds)

    visualiseWide(robot, crates, bounds)

    return sum(100 * y + x for x, y in crates)


def doWideMove(robot, move, crates, bounds):
    deltas = moveMap[move]
    newPos = (robot[0] + deltas[0], robot[1] + deltas[1])

    # print(f"Moving robot {move} from {robot} to {newPos}")
    # visualiseWide(robot, crates, bounds)

    if newPos in bounds:
        return robot

    fullCrates = crates | {(c[0]+1, c[1]) for c in crates}
    if newPos not in fullCrates:
        return newPos

    # moving crate right? newPos different
    nextCrate = newPos if newPos in crates else (newPos[0]-1, newPos[1])
    assert nextCrate in crates
    affected = set()
    can = canMoveCrate(nextCrate, move, crates, bounds, affected)
    if can:
        cratesBefore = len(crates)
        for c in affected:
            crates.remove(c)
        for c in affected:
            crates.add((c[0]+deltas[0], c[1] + deltas[1]))
        assert cratesBefore == len(crates), f"{cratesBefore=}, {affected=}, {len(crates)=} {crates}"
        return newPos
    return robot


def canMoveCrate(crate, move, crates, bounds, affected):
    deltas = moveMap[move]
    newPos = (crate[0] + deltas[0], crate[1] + deltas[1])
    fullCrate = {newPos, (newPos[0] + 1, newPos[1])}

    if not bounds.isdisjoint(fullCrate):
        # print(f"  Crate {crate} CAN'T move {move} to {newPos} — hits the wall")
        return False

    fullCrates = crates - {crate}
    fullCrates |= {(c[0]+1, c[1]) for c in fullCrates}
    if fullCrates.isdisjoint(fullCrate):
        # print(f"  Crate {crate} CAN move {move} to {newPos} — vacant")
        affected.add(crate)
        return True

    can = True
    if move in "<>":
        nextCrate = (newPos[0]+deltas[0], newPos[1]+deltas[1])
        if nextCrate not in crates:
            nextCrate = (nextCrate[0]-1, nextCrate[1])
        # print(f"    Shunting {nextCrate} trying to move crate {crate} {move} to {newPos}")
        assert crate != nextCrate
        assert crate in crates
        can = canMoveCrate(nextCrate, move, crates, bounds, affected)
    else:
        nextCrateLeft = (newPos[0], newPos[1]) if newPos in crates else (newPos[0]-1, newPos[1])
        nextCrateRight = (newPos[0]+1, newPos[1])
        if nextCrateLeft in crates:
            can = canMoveCrate(nextCrateLeft, move, crates, bounds, affected)
        if can and nextCrateRight in crates:
            can = canMoveCrate(nextCrateRight, move, crates, bounds, affected)

    if can:
        affected.add(crate)
    else:
        affected.clear()

    return can


def visualiseWide(robot, crates, bounds):
    for y in range(max(b[1] for b in bounds)+1):
        row = []
        for x in range(max(b[0] for b in bounds)+1):
            tile = (x, y)
            if tile in bounds:
                row.append("#")
            elif tile in crates:
                row.append("[")
            elif (tile[0]-1, tile[1]) in crates:
                row.append("]")
            elif tile == robot:
                row.append("@")
            else:
                row.append(".")
        print("".join(row))
