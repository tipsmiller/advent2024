import math
from dataclasses import dataclass

example = """
............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............
"""

@dataclass()
class Position:
    x: int
    y: int

    def isInSpace(self, space: [[str]]) -> bool:
        return 0 <= self.x < len(space[0]) and 0 <= self.y < len(space)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __add__(self, other):
        return Position(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Position(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        if isinstance(other, int):
            return Position(self.x * other, self.y * other)

    __rmul__ = __mul__

    def __truediv__(self, other):
        if isinstance(other, int):
            return Position(int(self.x / other), int(self.y / other))

    def __hash__(self):
        return hash((self.x, self.y))

@dataclass()
class Antenna:
    pos: Position
    freq: str

def getSpace(input: str) -> [[str]]:
    lines = input.strip().splitlines()
    lines = [list(line) for line in lines]
    print(f'parsed {len(lines)} lines')
    return lines

def getAntennae(space: [[str]]) -> {str, Antenna}:
    antennae = {}
    for y in range(len(space)):
        for x in range(len(space[0])):
            freq = space[y][x]
            if freq != '.':
                antennae.setdefault(freq, []).append(Antenna(Position(x, y), freq))
    print(f'found {len(antennae)} frequencies')
    return antennae

def getVector(pos1: Position, pos2: Position, harmonic: int) -> Position:
    return harmonic * (pos2 - pos1)

def findAntinodes(space: [[str]], antennae: {str, Antenna}) -> [Position]:
    antinodes = set()
    for freq, ants in antennae.items():
        # find the vector from each antenna to each other antenna
        # double the vector to locate an antinode
        for a1 in ants:
            otherAntennae = ants[:ants.index(a1)] + ants[ants.index(a1) + 1:]
            for a2 in otherAntennae:
                vec = getVector(a1.pos, a2.pos, 2)
                antinodes.add(a1.pos + vec)
                antinodes.add(a2.pos - vec)
    antinodes = [an for an in antinodes if an.isInSpace(space)]
    print(f'found {len(antinodes)} antinodes')
    return antinodes

def findAntinodesPart2(space: [[str]], antennae: {str, Antenna}) -> [Position]:
    antinodes = set()
    for freq, ants in antennae.items():
        # find the vector from each antenna to each other antenna
        # look for harmonics from 1:inf to locate each antinode
        for a1 in ants:
            otherAntennae = ants[:ants.index(a1)] + ants[ants.index(a1) + 1:]
            for a2 in otherAntennae:
                harmonic = 0
                baseVector = getVector(a1.pos, a2.pos, 1)
                divisor = math.gcd(baseVector.x, baseVector.y)
                baseVector = baseVector / divisor
                while True:
                    vec = baseVector * harmonic
                    antinode1 = a1.pos + vec
                    if antinode1.isInSpace(space):
                        antinodes.add(antinode1)
                    antinode2 = a1.pos - vec
                    if antinode2.isInSpace(space):
                        antinodes.add(antinode2)
                    if not antinode1.isInSpace(space) and not antinode2.isInSpace(space):
                        break
                    harmonic += 1
    antinodes = [an for an in antinodes if an.isInSpace(space)]
    print(f'found {len(antinodes)} antinodes')
    return antinodes


if __name__ == "__main__":
    # part 1 example
    space = getSpace(example)
    antennae = getAntennae(space)
    findAntinodes(space, antennae)

    # part 1
    space = getSpace(open('input.txt').read())
    antennae = getAntennae(space)
    findAntinodes(space, antennae)

    # part 2 example
    space = getSpace(example)
    antennae = getAntennae(space)
    findAntinodesPart2(space, antennae)

    # part 2
    space = getSpace(open('input.txt').read())
    antennae = getAntennae(space)
    findAntinodesPart2(space, antennae)

