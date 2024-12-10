from dataclasses import dataclass

example = """
2333133121414131402
"""

def doPart1(text: str):
    text = text.strip()
    files = []
    freespaces = []
    newDrive = []
    for i in range(len(text)):
        if i % 2 == 0:
            files.append(int(text[i]))
            newDrive.extend(str(int(i/2)) for f in range(files[-1]))
        else:
            freespaces.append(int(text[i]))
            newDrive.extend('.' * freespaces[-1])
    print(f'found {len(files)} files')
    print(f'found {len(freespaces)} free spaces')
    # print(f'new drive: {"".join(newDrive)}')

    frontIndex = 0
    backIndex = len(newDrive) - 1
    while True:
        while newDrive[frontIndex] != '.':
            frontIndex += 1
        while newDrive[backIndex] == '.':
            backIndex -= 1
        if frontIndex >= backIndex:
            break
        newDrive[frontIndex] = newDrive[backIndex]
        newDrive[backIndex] = '.'
        #print(f'drive state: {"".join(newDrive)}')
    # print(f'drive state: {"".join(newDrive)}')
    print(f'score: {sum(i * int(newDrive[i]) for i in range(len(newDrive)) if newDrive[i] != ".")}')

@dataclass
class Space:
    id: int
    length: int

    def __str__(self) -> str:
        return '.' * self.length

@dataclass
class File:
    id: int
    length: int

    def __str__(self) -> str:
        return str(self.id) * self.length

def doPart2(text: str):
    text = text.strip()
    drive = []
    files = []
    spaces = []
    for i in range(len(text)):
        if i % 2 == 0:
            file = File(i//2, int(text[i]))
            drive.append(file)
            files.append(file)
        else:
            space = Space(i//2+1, int(text[i]))
            drive.append(space)
            if space.length > 0:
                spaces.append(space)
    # print(f'new drive: {"".join(str(f) for f in drive)}')
    # print(f'drive length: {sum(f.length for f in drive)}')

    # start with the last file
    # try to find a place to put it, starting from the front
    fileIndex = 0
    spaceIndex = 0
    for file in reversed(files):
        print(f'working on file {file.id}')
        for space in spaces:
            if space.length < file.length:
                continue
            fileIndex = drive.index(file)
            spaceIndex = drive.index(space)
            if fileIndex < spaceIndex:
                break
            # shrink the space
            space.length -= file.length
            if space.length == 0:
                spaces.remove(space)
            # move the file
            drive.insert(spaceIndex, drive.pop(fileIndex))
            # expand space where the file was
            assert isinstance(drive[fileIndex], Space)
            drive[fileIndex].length += file.length
            break
        # print(f'drive state: {"".join(str(f) for f in drive)[:100]}')

    score = 0
    index = 0
    for file in drive:
        for block in range(file.length):
            if not isinstance(file, Space):
                score += index * file.id
            index += 1
    print(f'checksum: {score}')

if __name__ == "__main__":
    # part 1 example
    doPart1(example)

    # part 1
    doPart1(open('input.txt').read())

    # part 2 example
    doPart2(example)

    # part 2 example
    doPart2(open('input.txt').read())
