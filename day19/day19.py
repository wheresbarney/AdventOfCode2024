# https://adventofcode.com/2024/day/19

from functools import lru_cache


def q1(lines):
    towels = frozenset({t.strip() for t in lines[0].split(",")})
    patterns = [l for l in lines[2:]]

    def possible(pattern):
        for towel in towels:
            if towel == pattern:
                return True
            if pattern.startswith(towel) and possible(pattern[len(towel) :]):
                return True

        return False

    return len(tuple(filter(possible, patterns)))


def q2(lines):
    towels = frozenset({t.strip() for t in lines[0].split(",")})
    patterns = [l for l in lines[2:]]

    @lru_cache
    def permutations(pattern):
        perms = 0
        for towel in towels:
            if towel == pattern:
                perms += 1
            elif pattern.startswith(towel):
                perms += permutations(pattern[len(towel) :])

        return perms

    return sum(map(permutations, patterns))
