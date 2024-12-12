# https://adventofcode.com/2024/day/12


from dataclasses import dataclass


def q1(input):
    visited = set()
    fences = 0

    for y in range(len(input)):
        for x in range(len(input[y])):
            area, perimeter = measurePlot(input, x, y, visited)
            fences += perimeter * area
    return fences

def measurePlot(input, x, y, visited, cumPerimeter=0, cumArea=0):
    if (x, y) in visited:
        return cumPerimeter, cumArea
    visited.add((x, y))

    cumArea += 1
    for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        if y+dy < 0 or y+dy >= len(input) or x+dx < 0 or x+dx >= len(input[y+dy]):
            cumPerimeter += 1
        elif input[y+dy][x+dx] != input[y][x]:
            cumPerimeter += 1
        else:
            cumPerimeter, cumArea = measurePlot(input, x+dx, y+dy, visited, cumPerimeter, cumArea)
    return cumPerimeter, cumArea


@dataclass
class Boundary:
    direction: str
    points: set[tuple[int, int]]

    def adjacentTo(self, direction, x, y):
        if self.direction != direction:
            return False
        if self.direction in "<>":
            return self.points & {(x, y-1), (x, y+1)}
        return self.points & {(x-1, y), (x+1, y)}


def q2(input):
    visited = set()
    fences = 0

    for y in range(len(input)):
        for x in range(len(input[y])):
            edges, area = measurePlotByEdge(input, x, y, visited, [], 0)
            fences += edges * area
    return fences


# edges is a list of known edges of the current plot
# it's a tuple of d, x, y where
# d is the direction of the edge: <>^v for left edge, right edge, top edge, bottom edge
# x & y are the coordinates of the cell to which it applies
def measurePlotByEdge(input, x, y, visited, edges, cumArea):
    if (x, y) in visited:
        return len(edges), cumArea
    visited.add((x, y))

    cumArea += 1
    for dx, dy, d in [(0, 1, "v"), (0, -1, "^"), (1, 0, ">"), (-1, 0, "<")]:
        if y+dy < 0 or y+dy >= len(input) or x+dx < 0 or x+dx >= len(input[y+dy]) or input[y+dy][x+dx] != input[y][x]:
            # found an edge
            # is it a new edge?
            existing = list(filter(lambda b: b.adjacentTo(d, x, y), edges))
            if len(existing) == 1:
                # print(f"{[x, y]}:{input[y][x]} extending {d} boundary")
                existing[0].points.add((x, y))
            elif len(existing) == 2:
                # print(f"{[x, y]}:{input[y][x]} joining boundaries {existing}")
                edges.remove(existing[0])
                existing[1].points.update(existing[0].points)
                existing[1].points.add((x, y))
            else:
                # print(f"{[x, y]}:{input[y][x]} creating {d} boundary")
                edges.append(Boundary(d, {(x, y)}))

    for dx, dy, d in [(0, 1, "v"), (0, -1, "^"), (1, 0, ">"), (-1, 0, "<")]:
        if y+dy >= 0 and y+dy < len(input) and x+dx >= 0 and x+dx < len(input[y+dy]) and input[y+dy][x+dx] == input[y][x]:
            _, cumArea = measurePlotByEdge(input, x+dx, y+dy, visited, edges, cumArea)
    return len(edges), cumArea
