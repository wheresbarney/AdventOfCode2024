# https://adventofcode.com/2024/day/22


def q1(lines):
    secrets = [int(l) for l in lines]
    total = 0
    for secret in secrets:
        for _ in range(2000):
            secret ^= (secret << 6) % 2**24  # 2^6 = 64
            secret ^= (secret >> 5) % 2**24  # 2^5 = 32
            secret ^= (secret << 11) % 2**24  # 2^11 = 2048
        total += secret
    return total


def q2(lines):
    secrets = [int(l) for l in lines]
    monkeys = []
    for secret in secrets:
        monkeys.append([secret % 10])
        for _ in range(2000):
            secret ^= (secret << 6) % 2**24  # 2^6 = 64
            secret ^= (secret >> 5) % 2**24  # 2^5 = 32
            secret ^= (secret << 11) % 2**24  # 2^11 = 2048
            monkeys[-1].append(secret % 10)

    seqMaps = [makeSeqMap(m) for m in monkeys]

    bestSeqs = set()
    for monkey in monkeys:
        bestSeqs |= findBestSequences(monkey)

    bananas = 0
    for i, seq in enumerate(bestSeqs):
        bananas = max(bananas, evaluateSequence(seq, seqMaps))
        # print(f"{i}/{len(bestSeqs)}: evaluated {seq}, bananas now {bananas}")

    return bananas


def findBestSequences(prices):
    highest = 0
    best = set()
    for i in range(4, len(prices)):
        if prices[i] > highest:
            highest = prices[i]
            best = {
                tuple(prices[i - j] - prices[i - j - 1] for j in reversed(range(4)))
            }
        elif prices[i] == highest:
            best.add(
                tuple(prices[i - j] - prices[i - j - 1] for j in reversed(range(4)))
            )
    return best


def makeSeqMap(prices):
    seqMap = {}  # dictionary of sequence to first price for that sequence
    for i in range(4, len(prices)):
        seq = tuple(prices[i - j] - prices[i - j - 1] for j in reversed(range(4)))
        if seq not in seqMap:
            seqMap[seq] = prices[i]
    return seqMap


def evaluateSequence(seq, seqMaps):
    return sum(seqMap.get(seq, 0) for seqMap in seqMaps)
