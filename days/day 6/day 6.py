import pprint
import timeit
from dataclasses import dataclass
import copy

example = """
....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#...
"""

DIRECTIONS = [
    [0, -1], # up
    [1, 0],  # right
    [0, 1],  # down
    [-1, 0]  # left
]

@dataclass()
class Position:
    x: int
    y: int

    def getObjectAtPosition(self, room: [[str]]) -> str:
        if self.isInRoom(room):
            return room[self.y][self.x]
        return None

    def isInRoom(self, room: [[str]]) -> bool:
        return 0 <= self.x < len(room[0]) and 0 <= self.y < len(room)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))

class Guard:
    pos: Position
    dir = None
    steps = 0

    def __init__(self, position: Position):
        self.pos = position
        self.dir = DIRECTIONS[0]

    def turn(self):
        turnIndex = DIRECTIONS.index(self.dir) + 1
        if turnIndex == len(DIRECTIONS):
            turnIndex = 0
        self.dir = DIRECTIONS[turnIndex]

    def walk(self):
        self.pos = Position(self.pos.x + self.dir[0], self.pos.y + self.dir[1])
        self.steps += 1

    def __eq__(self, other):
        return self.pos == other.pos and self.dir == other.dir

    def __hash__(self):
        return hash((self.pos, self.dir[0], self.dir[1]))

def readMap(input: str) -> [[str]]:
    lines = [list(line) for line in input.strip().splitlines()]
    return lines

def findGuard(room: [[str]]) -> (int, int):
    for y in range(len(room)):
        try:
            return Guard(Position(room[y].index('^'), y))
        except ValueError:
            continue

# returns True if the guard leaves the room, False if not
def iterateGuard(guard: Guard, room: [[str]]) -> bool:
    # will iterate the guard's position, leaving 'X' behind in the room
    previousStates = set()
    while guard.pos.isInRoom(room):
        previousStates.add(guard)
        room[guard.pos.y][guard.pos.x] = 'X'
        # check for collision
        turns = 0
        while turns < 4:
            nextPosition = Position(guard.pos.x + guard.dir[0], guard.pos.y + guard.dir[1])
            if nextPosition.getObjectAtPosition(room) == '#':
                # found an obstacle, turn
                guard.turn()
                turns += 1
            else:
                guard.walk()
                break
        if turns == 4:
            return False
        if guard in previousStates:
            return False
    return True

def countVisitedPositions(room: [[str]]) -> int:
    return sum(sum(x == "X" for x in row) for row in room)

def doPart1(input: str):
    room = readMap(input)
    #pprint.pprint(room)
    guard = findGuard(room)
    #print((guard.pos.x, guard.pos.y), room[guard.pos.y][guard.pos.x])
    iterateGuard(guard, room)
    #pprint.pprint(room)
    print(f'score: {countVisitedPositions(room)}')

def findObjectPositions(room: [[str]]) -> set[Position]:
    # Find positions where an object can be placed
    validPositions = set()
    for y in range(len(room)):
        for x in range(len(room[0])):
            pos = Position(x, y)
            if pos.getObjectAtPosition(room) == 'X':
                validPositions.add(pos)
    return validPositions

def doPart2(input: str):
    room = readMap(input)
    guard = findGuard(room)
    traversedRoom = copy.deepcopy(room)
    iterateGuard(copy.deepcopy(guard), traversedRoom)
    # only need the positions the guard can actually reach
    validPositions = findObjectPositions(traversedRoom)
    # exclude the starting position
    validPositions -= {guard.pos}
    print(f'found {len(validPositions)} valid positions')
    looperPositions = []
    for pos in validPositions:
        modifiedRoom = copy.deepcopy(room)
        modifiedRoom[pos.y][pos.x] = '#'
        if not iterateGuard(copy.deepcopy(guard), modifiedRoom):
            looperPositions.append(pos)
    print(f'found {len(looperPositions)} looper positions')

if __name__ == "__main__":
    # part 1 example
    time = timeit.timeit(lambda: doPart1(example), number=1)
    print(f'time: {time}')

    # part 1
    time = timeit.timeit(lambda: doPart1(open('input.txt').read()), number=1)
    print(f'time: {time}')

    # part 2 example
    time = timeit.timeit(lambda: doPart2(example), number=1)
    print(f'time: {time}')

    # part 2
    time = timeit.timeit(lambda: doPart2(open('input.txt').read()), number=1)
    print(f'time: {time}')