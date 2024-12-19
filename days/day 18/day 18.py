from copy import copy
from dataclasses import dataclass
from pprint import pprint

example1 = """
5,4
4,2
4,5
3,0
2,1
6,3
2,4
1,5
0,6
3,3
2,6
5,1
1,2
5,5
2,5
6,5
1,4
0,4
6,4
1,1
6,1
1,0
0,5
1,6
2,0
"""

@dataclass()
class Position:
    x: int
    y: int

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

Space = {Position: str}

DIRECTIONS = [
    Position(1, 0),  # right
    Position(0, 1),  # down
    Position(-1, 0), # left
    Position(0, -1), # up
]

COMMANDS = {
    '>': DIRECTIONS[0],
    'v': DIRECTIONS[1],
    '<': DIRECTIONS[2],
    '^': DIRECTIONS[3],
}

class AStarNode:
    position: Position
    prev: [Position] # a list of states that could lead here
    g: int
    h: int

    def __init__(self, position, prev, g, end):
        self.position = position
        self.prev = prev
        self.g = g
        self.h = self.calcH(end)

    def __eq__(self, other):
        if other is None:
            return False
        return self.position == other.position and self.g == other.g and self.h == other.h

    def __hash__(self):
        return hash((self.position, self.g, self.h))

    def calcH(self,  end: Position):
        return abs(end.x - self.position.x) + abs(end.y - self.position.y)

    def f(self):
        return self.g + self.h

def printSpace(space: Space, size: (int, int)):
    for y in range(size[1]):
        print(''.join(list(space[Position(x, y)] for x in range(size[0]))))

def findPath(startNode: AStarNode, end: Position, space: Space):
    openNodes = {startNode.position: startNode}
    closedNodes = {}
    while len(openNodes) > 0:
        # if printSteps:
        #     displaySpace = copy.deepcopy(space)
        #     for node in openNodes.values():
        #         displaySpace[node.state.pos] = node.cost
        #     for node in closedNodes:
        #         displaySpace[node.state.pos] = node.cost
        #     printSpace(displaySpace)
        currentNode = sorted(openNodes.values(), key=lambda node: node.f())[0]
        del openNodes[currentNode.position]
        closedNodes[currentNode.position] = currentNode
        if currentNode.position == end:
            return closedNodes
        for direction in DIRECTIONS:
            neighbor = AStarNode(currentNode.position + direction,  currentNode.prev + [currentNode.position], currentNode.g + 1, end)
            if neighbor.position not in space or space[neighbor.position] == '#' or neighbor.position in closedNodes:
                continue
            if neighbor.position not in openNodes or neighbor.f() < openNodes[neighbor.position].f():
                openNodes[neighbor.position] = neighbor

def doTheThing(spaceSize: (int, int), text: str, numBytesToFall, printProgress=False, partTwo=False, expectedScore=None):
    space = {}
    for x in range(spaceSize[0]):
        for y in range(spaceSize[1]):
            space[Position(x, y)] = '.'
    bytePositions = [Position(int(line.split(',')[0]), int(line.split(',')[1])) for line in text.strip().splitlines()]
    print(f'loaded {len(bytePositions)} bytes to fall')
    start = Position(0, 0)
    end = Position(spaceSize[0]-1, spaceSize[1]-1)
    assert start in space and end in space
    closedNodes = findPath(AStarNode(start, [], 0, end), end, space)
    lastScore = None
    for i in range(numBytesToFall):
        # drop a byte on the space.
        # if it's in the end node's previous states, those have to be put back on the open nodes
        bytePosition = bytePositions[i]
        space[bytePosition] = '#'
        if bytePosition in closedNodes[end].prev:
            closedNodes = findPath(AStarNode(start, [], 0, end), end, space)
            if closedNodes is None:
                print(f'Dropped {i} bytes before the exit was closed: last byte was {bytePositions[i]}')
                break
            lastScore = closedNodes[end].f()
    print(f'Got score: {lastScore}')

if __name__ == "__main__":
    # examples
    doTheThing((7, 7), example1, 12)

    # part 1
    doTheThing((71, 71), open('input.txt').read(), 1024)

    # part 2
    doTheThing((7, 7), example1, 25)

    # part 1
    doTheThing((71, 71), open('input.txt').read(), 3450)
