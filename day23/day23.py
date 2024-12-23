# https://adventofcode.com/2024/day/23

from pprint import PrettyPrinter


def q1(lines):
    connections = {}
    for l, r in [line.split("-") for line in lines]:
        connections.setdefault(l, set()).add(r)
        connections.setdefault(r, set()).add(l)

    sets_of_three_with_t = set()
    for comp, conns in connections.items():
        if comp[0] != "t":
            continue
        for comp2 in conns:
            for comp3 in conns:
                if comp3 in connections[comp2]:
                    sets_of_three_with_t.add(tuple(sorted([comp, comp2, comp3])))
    return len(sets_of_three_with_t)


def q2(lines):
    connections = {}
    for l, r in [line.split("-") for line in lines]:
        connections.setdefault(l, set()).add(r)
        connections.setdefault(r, set()).add(l)

    def is_party(comps):
        for comp in comps:
            if not (connections[comp] | {comp}).issuperset(comps):
                return False
        return True

    def find_largest_party(comps, party):
        nonlocal largest_party
        if not is_party(party):
            return
        if len(party) > len(largest_party):
            print(f"Largest party so far [{len(party)}]: {sorted(party)}")
            largest_party = party

        for i in range(len(comps)):
            find_largest_party(comps[i + 1 :], party | {comps[i]})

    largest_party = set()
    find_largest_party(list(connections.keys()), set())
    return ",".join(sorted(largest_party))
