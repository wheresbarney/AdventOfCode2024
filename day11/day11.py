# https://adventofcode.com/2024/day/11


from collections import deque, defaultdict


def q1(lines):
    stones = [int(s) for s in lines[0].split()]

    for _ in range(25):
        newstones = []
        for i, s in enumerate(stones):
            ss = str(s)

            if s == 0:
                stones[i] = 1
            elif len(ss) % 2 != 0:
                stones[i] *= 2024
            else:
                stones[i] = int(ss[:len(ss)//2])
                newstones.append((i+1+len(newstones), int(ss[len(ss)//2:])))

        for p, s in newstones:
            stones.insert(p, s)

    return len(stones)


def q2(lines):
    stones = {int(s): 1 for s in lines[0].split()}
    for _ in range(75):
        newstones = defaultdict(int)
        for stone, count in stones.items():
            ss = str(stone)

            if stone == 0:
                newstones[1] += count
            elif len(ss) % 2 != 0:
                newstones[stone * 2024] += count
            else:
                newstones[int(ss[:len(ss)//2])] += count
                newstones[int(ss[len(ss)//2:])] += count
        stones = newstones

    return sum(stones.values())


def q2_memoised(lines):
    loops = 75
    # terminals = []
    # lines = ["17"]
    stones = deque([(int(s), 0) for s in lines[0].split()])
    count = len(stones)
    memo = {} # n -> (splits_after, left, right)
    while stones:
        stone, generation = stones.popleft()
        orig_s, orig_n = stone, generation
        while generation < loops:
            if stone in memo:
                splits_after, left, right = memo[stone]
                if generation + splits_after <= loops:
                    # print(f"using memo {generation=} {stone=}: {memo[stone]}")
                    stone = left
                    generation += splits_after
                    stones.append((right, generation))
                    orig_s, orig_n = stone, generation
                    count += 1
                    continue

            generation += 1
            ss = str(stone)
            if stone == 0:
                stone = 1
            elif len(ss) % 2 != 0:
                stone *= 2024
            else:
                left = int(ss[:len(ss)//2])
                right = int(ss[len(ss)//2:])
                stones.append((right, generation))
                if orig_s <10000:
                    # print(f"memoising {orig_s} => {stone} => {left},{right} after {generation}-{orig_n}=>{generation-orig_n} generations")
                    memo[orig_s] = (generation - orig_n, left, right)
                stone = left
                orig_s, orig_n = stone, generation
                count += 1
        # if generation == loops:
        #     terminals.append(stone)
    # print(terminals)
    return count


# def q2(lines):
#     generations = 75
#     stones = deque([(int(s), generations) for s in lines[0].split()])
#     count = len(stones)
#     while stones:
#         stone, generation = stones.popleft()
#         terminals, additions = applyRules(stone, generation)
#         count += terminals
#         stones.extend(additions)

#     return count


# def applyRules(stone, generation):
#     ss = str(stone)
#     if stone == 0:
#         stone = 1
#     elif len(ss) % 2 != 0:
#         stone *= 2024
#     else:
#         left = int(ss[:len(ss)//2])
#         right = int(ss[len(ss)//2:])
#         return (1, [(left, generation), (right, generation)])


# def q2_linkedlist(lines):
#     stones = None
#     count = 0
#     for s in reversed(lines[0].split()):
#         stones = ListNode(int(s), stones)
#         count += 1
#     assert stones is not None

#     for n in range(75):
#         newstones = []
#         stone = stones
#         while stone:
#             ss = str(stone.data)

#             if stone.data == 0:
#                 stone.data = 1
#             elif len(ss) % 2 != 0:
#                 stone.data *= 2024
#             else:
#                 stone.data = int(ss[:len(ss)//2])
#                 newstones.append((stone, int(ss[len(ss)//2:])))
#             stone = stone.next

#         for s, ns in newstones:
#             s.next = ListNode(ns, s.next)
#             count += 1

#         if n % 5 == 0:
#             print(f"{n=} {count=}")


#     return count


# class ListNode:
#     """
#     A node in a singly-linked list.
#     """
#     def __init__(self, data=None, next=None):
#         self.data = data
#         self.next = next

#     def __repr__(self):
#         return (f"{repr(self.data)} -> {self.next if self.next else ''}")

#     def __iter__(self):
#         return ListNodeIterator(self)


# class ListNodeIterator:
#     def __init__(self, node):
#         self.node = node

#     def __next__(self):
#         if self.node is not None:
#             data = self.node.data
#             self.node = self.node.next
#             return data
#         else:
#             raise StopIteration
