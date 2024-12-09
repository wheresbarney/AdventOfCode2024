# https://adventofcode.com/2024/day/9


from dataclasses import dataclass


@dataclass
class FileHandle:
    position: int
    length: int
    id: int


@dataclass
class SpaceHandle:
    position: int
    length: int


def q1(lines):
    files = []
    freespace = []
    position = 0
    for i in range(len(lines[0])):
        if i % 2 == 0:
            files.append(FileHandle(position, int(lines[0][i]), i // 2))
        else:
            freespace.append(SpaceHandle(position, int(lines[0][i])))
        position += int(lines[0][i])

    while len(freespace):
        free = freespace.pop(0)
        while free.length > 0:
            lastFile = files[-1]
            if free.position > lastFile.position:
                break

            if lastFile.length <= free.length:
                # print(f"Moving {lastFile} into {free}")
                lastFile.position = free.position
                files.sort(key=lambda x: x.position)
                free.position += lastFile.length
                free.length -= lastFile.length
                # print(f"  -> {lastFile}, {free}")
            else:
                # print(f"Splitting {lastFile} into {free}")
                lastFile.length -= free.length
                newFile = FileHandle(free.position, free.length, lastFile.id)
                files.append(newFile)
                files.sort(key=lambda x: x.position)
                free.length = 0
                # print(f"  -> {newFile}, {lastFile}")

    checkSum = 0
    contiguous = 0
    for file in files:
        assert file.position == contiguous, f"{file} {contiguous}"
        contiguous += file.length
        for i in range(file.length):
            checkSum += file.id * (file.position + i)

    return checkSum


def q2(lines):
    files = []
    freespace = []
    position = 0
    for i in range(len(lines[0])):
        if i % 2 == 0:
            files.append(FileHandle(position, int(lines[0][i]), i // 2))
        else:
            freespace.append(SpaceHandle(position, int(lines[0][i])))
        position += int(lines[0][i])

    for file in reversed(files):
        for free in freespace:
            if file.length <= free.length and file.position > free.position:
                file.position = free.position
                free.length -= file.length
                free.position += file.length
                break

    files.sort(key=lambda x: x.position)
    checkSum = 0
    for file in files:
        for i in range(file.length):
            checkSum += file.id * (file.position + i)

    return checkSum
