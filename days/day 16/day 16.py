import copy
from dataclasses import dataclass
from pprint import pprint
from typing import Union

example1 = """
###############
#.......#....E#
#.#.###.#.###.#
#.....#.#...#.#
#.###.#####.#.#
#.#.#.......#.#
#.#.#####.###.#
#...........#.#
###.#.#####.#.#
#...#.....#.#.#
#.#.#.###.#.#.#
#.....#...#.#.#
#.###.#.#.#.#.#
#S..#.....#...#
###############
"""

example2 = """
#################
#...#...#...#..E#
#.#.#.#.#.#.#.#.#
#.#.#.#...#...#.#
#.#.#.#.###.#.#.#
#...#.#.#.....#.#
#.#.#.#.#.#####.#
#.#...#.#.#.....#
#.#.#####.#.###.#
#.#.#.......#...#
#.#.###.#####.###
#.#.#...#.....#.#
#.#.#.#####.###.#
#.#.#.........#.#
#.#.#.#########.#
#S#.............#
#################
"""

example3 = """
###########################
#######################..E#
######################..#.#
#####################..##.#
####################..###.#
###################..##...#
##################..###.###
#################..####...#
################..#######.#
###############..##.......#
##############..###.#######
#############..####.......#
############..###########.#
###########..##...........#
##########..###.###########
#########..####...........#
########..###############.#
#######..##...............#
######..###.###############
#####..####...............#
####..###################.#
###..##...................#
##..###.###################
#..####...................#
#.#######################.#
#S........................#
###########################
"""

example4 = """
##########
#.......E#
#.##.#####
#..#.....#
##.#####.#
#S.......#
##########
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

@dataclass
class State:
    pos: Position
    direction: Position

    def __eq__(self, other):
        return self.pos == other.pos and self.direction == other.direction

    def __hash__(self):
        return hash((self.pos, self.direction))

Space = {Position: Union[str, any]}

DIRECTIONS = [
    Position(1, 0),  # right
    Position(0, 1),  # down
    Position(-1, 0), # left
    Position(0, -1), # up
]

ARROWS = {
    '>': DIRECTIONS[0],
    'v': DIRECTIONS[1],
    '<': DIRECTIONS[2],
    '^': DIRECTIONS[3],
}

NEXT_DIRECTION = {
    Position(1, 0): Position(0, 1),
    Position(0, 1): Position(-1, 0),
    Position(-1, 0): Position(0, -1),
    Position(0, -1): Position(1, 0),
}

def getSpace(text: str) -> (Space, {str}):
    lines = text.strip().splitlines()
    space = {}
    xSize, ySize = len(lines[0]), len(lines)
    for y in range(ySize):
        for x in range(xSize):
            space[Position(x, y)] = lines[y][x]
    return space, (xSize, ySize)

def printSpace(space: Space):
    out = []
    sizeX = max(pos.x for pos in space)
    sizeY = max(pos.y for pos in space)
    for y in range(sizeY + 1):
        out.append(''.join(list(str(space[Position(x, y)]).ljust(6, ' ') for x in range(sizeX + 1))))
    pprint(out, width=200)

class AStarNode:
    state: State
    prev: {State} # a set of states that could lead here
    cost: int

    def __init__(self, state, prev, cost):
        self.state = state
        self.prev = prev
        self.cost = cost

    def __eq__(self, other):
        if other is None:
            return False
        return self.state == other.state and self.cost == other.cost

    def __hash__(self):
        return hash(self.state)

def search(space: Space, start: State, printSteps: bool) -> {State: AStarNode}:
    startNode = AStarNode(start, set(), 0)
    openNodes = {startNode.state: startNode}
    closedNodes = {}
    while len(openNodes) > 0:
        if printSteps:
            displaySpace = copy.deepcopy(space)
            for node in openNodes.values():
                displaySpace[node.state.pos] = node.cost
            for node in closedNodes:
                displaySpace[node.state.pos] = node.cost
            printSpace(displaySpace)
        currentNode = sorted(openNodes.values(), key=lambda node: node.cost)[0]
        del openNodes[currentNode.state]
        closedNodes[currentNode.state] = currentNode
        neighbors = [
            AStarNode(State(currentNode.state.pos + currentNode.state.direction, currentNode.state.direction), {currentNode.state}, currentNode.cost + 1),
            AStarNode(State(currentNode.state.pos, NEXT_DIRECTION[currentNode.state.direction]), {currentNode.state}, currentNode.cost + 1000),
            AStarNode(State(currentNode.state.pos, NEXT_DIRECTION[NEXT_DIRECTION[NEXT_DIRECTION[currentNode.state.direction]]]), {currentNode.state}, currentNode.cost + 1000)
        ]
        for neighbor in neighbors:
            if space[neighbor.state.pos] == '#':
                continue
            if neighbor.state in closedNodes:
                if neighbor.cost == closedNodes[neighbor.state].cost:
                    closedNodes[neighbor.state].prev.add(currentNode.state)
                continue
            if neighbor.state not in openNodes or neighbor.cost < openNodes[neighbor.state].cost:
                openNodes[neighbor.state] = neighbor
            elif neighbor.cost == openNodes[neighbor.state].cost:
                openNodes[neighbor.state].prev.add(currentNode.state)
    return closedNodes

def doTheThing(spaceText: str, printSteps=False, partTwo=False, expectedScore=None, expectedPositions=None):
    space, size = getSpace(spaceText)
    startState = State(Position(1, size[1]-2), ARROWS['>'])
    space[startState.pos] = 0
    endPosition = Position(size[0]-2, 1)
    closedNodes = search(space, startState, printSteps)
    endStates = [state for state in closedNodes if state.pos == endPosition]
    scores = [closedNodes[e].cost for e in endStates]
    print(f'Got scores: {[closedNodes[e].cost for e in endStates]}')
    minScore = min(scores)
    endStates = [state for state in endStates if closedNodes[state].cost == minScore]
    if not partTwo:
        if expectedScore:
            assert minScore == expectedScore
    else:
        states = set(endStates)
        nodes: [AStarNode] = [closedNodes[state] for state in endStates]
        while len(nodes) > 0:
            newNodes = []
            for node in nodes:
                for state in node.prev:
                    if state not in states:
                        states.add(state)
                        newNodes.append(closedNodes[state])
            nodes = newNodes
        positions = set(state.pos for state in states)
        if printSteps:
            displaySpace = copy.deepcopy(space)
            for pos in positions:
                displaySpace[pos] = 'O'
            printSpace(displaySpace)
        print(f'Got positions: {len(positions)}')
        if expectedPositions:
            assert len(positions) == expectedPositions


if __name__ == "__main__":
    # examples
    doTheThing(example1, expectedScore=7036)
    doTheThing(example2, expectedScore=11048)
    doTheThing(example3, expectedScore=21148)
    doTheThing(example4, expectedScore=4013)

    # part 1
    doTheThing(open('input.txt').read(), expectedScore=89460)

    # examples
    doTheThing(example1, partTwo=True, expectedPositions=45)
    doTheThing(example2, partTwo=True, expectedPositions=64)

    # part 2
    doTheThing(open('input.txt').read(), partTwo=True)
