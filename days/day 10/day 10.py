import copy
import pprint
from dataclasses import dataclass

example = """
89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732
"""

@dataclass()
class Position:
    x: int
    y: int

    def isInSpace(self, space: [[int]]) -> bool:
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

    def getValidSteps(self, space: [[int]], steps: {'Position'}):
        for direction in DIRECTIONS:
            step = self + direction
            if step.isInSpace(space) and space[step.y][step.x] == space[self.y][self.x] + 1 and step not in steps:
                steps.add(step)
                # print(f'took step to {step.x, step.y, space[step.y][step.x]}')
                if space[step.y][step.x] != 9:
                    step.getValidSteps(space, steps)


DIRECTIONS = [
    Position(1, 0),  # right
    Position(0, 1),  # down
    Position(-1, 0), # left
    Position(0, -1), # up
]

class Trailhead:
    start: Position
    ends: {Position}
    allSteps: {Position}
    allTrails: [[Position]]

    def __init__(self, start: Position):
        self.start = start
        self.ends = set()
        self.allSteps = {start}
        self.allTrails = []

    def searchForConnectedPeaks(self, space: [[int]]):
        self.start.getValidSteps(space, self.allSteps)
        self.ends = {p for p in self.allSteps if space[p.y][p.x] == 9}
        # self.printPaths(space)

    def numConnectedPeaks(self):
        return len(self.ends)

    def numTrails(self):
        return len(self.allTrails)

    def printPaths(self, space):
        print(f'all step values: {[space[pos.y][pos.x] for pos in self.allSteps]}')
        outSpace = [['.' for _ in row] for row in space]
        for pos in self.allSteps:
            outSpace[pos.y][pos.x] = space[pos.y][pos.x]
        pprint.pprint(outSpace)

    def printTrails(self, space):
        outSpace = [['.' for _ in row] for row in space]
        for trail in self.allTrails:
            for pos in trail:
                outSpace[pos.y][pos.x] = space[pos.y][pos.x]
        pprint.pprint(outSpace)


    def searchForValidTrails(self, space: [[int]]):
        self.allTrails = [[self.start]]
        while all(space[t[-1].y][t[-1].x] != 9 for t in self.allTrails):
            newTrails = []
            for trail in self.allTrails:
                trailEnd = trail[-1]
                currentValue = space[trailEnd.y][trailEnd.x]
                if currentValue == 9:
                    continue
                for direction in DIRECTIONS:
                    step = trailEnd + direction
                    if step.isInSpace(space) and space[step.y][step.x] == currentValue + 1:
                        newTrails.append(trail + [step])
            self.allTrails = newTrails
        # self.printTrails(space)


def getSpace(text: str) -> [[int]]:
    lines = text.strip().splitlines()
    space = [[int(pos) for pos in line] for line in lines]
    return space

def doPart1(text: str):
    trailheads = []
    space = getSpace(text)
    for y in range(len(space)):
        for x in range(len(space[y])):
            if space[y][x] == 0:
                trailheads.append(Trailhead(Position(x, y)))
    print(f'found {len(trailheads)} trailheads')
    totalScore = 0
    for th in trailheads:
        th.searchForConnectedPeaks(space)
        totalScore += th.numConnectedPeaks()
    print(f'total score: {totalScore}')


def doPart2(text: str):
    trailheads = []
    space = getSpace(text)
    for y in range(len(space)):
        for x in range(len(space[y])):
            if space[y][x] == 0:
                trailheads.append(Trailhead(Position(x, y)))
    print(f'found {len(trailheads)} trailheads')
    totalScore = 0
    for th in trailheads:
        th.searchForValidTrails(space)
        totalScore += th.numTrails()
    print(f'total score: {totalScore}')

if __name__ == "__main__":
    # part 1 example
    doPart1(example)

    # part 1
    doPart1(open('input.txt').read())

    # part 2 example
    doPart2(example)

    # part 2 example
    doPart2(open('input.txt').read())
