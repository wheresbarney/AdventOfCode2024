# https://adventofcode.com/2024/day/7


def q1(lines):
    total = 0
    for line in lines:
        test, args = line.split(":")
        test = int(test)
        args = [int(a) for a in args.split()]

        if hasPathToTest(args, test):
            total += test

    return total


def q2(lines):
    total = 0
    for line in lines:
        test, args = line.split(":")
        test = int(test)
        args = [int(a) for a in args.split()]

        if hasPathToTest(args, test, allowMerge=True):
            total += test

    return total


# DFS recursion into binary graph, left leg introduces one more mult op, right leg uses add in the same position
# optimisation: don't recurse further if we're already over total
# for a 4-arg example, there are three operators
#             a?b?c
#     a*b?c          a+b?c
# a*b*c   a*b+c   a+b*c   a+b+c
def hasPathToTest(args, test, operators=[], allowMerge=False):
    t = args[0]

    for i, op in enumerate(operators):
        if op == "*":
            t *= args[i + 1]
        elif op == "+":
            t += args[i + 1]

    if t > test:
        return False

    if len(operators) == len(args) - 1:
        return t == test

    if hasPathToTest(args, test, operators + ["*"], allowMerge) or hasPathToTest(
        args, test, operators + ["+"], allowMerge
    ):
        return True

    if allowMerge:
        mergePoint = len(operators)
        mergedArgs = [int(str(t) + str(args[mergePoint + 1]))] + args[mergePoint + 2 :]
        mergedOperators = operators[mergePoint + 2 :]

        return hasPathToTest(
            mergedArgs,
            test,
            mergedOperators,
            allowMerge,
        )
    return False
