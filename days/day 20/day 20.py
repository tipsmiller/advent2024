from dataclasses import dataclass

example1 = """
###############
#...#...#.....#
#.#.#.#.#.###.#
#S#...#.#.#...#
#######.#.#.###
#######.#.#...#
#######.#.###.#
###..E#...#...#
###.#######.###
#...###...#...#
#.#####.#.###.#
#.#...#.#.#...#
#.#.#.#.#.#.###
#...#...#...###
###############
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

QUADRANTS = [
    Position(1, 1),  # right
    Position(1, -1),  # down
    Position(-1, 1), # left
    Position(-1, -1), # up
]

def getSpace(text: str) -> (Space, Position, Position, (int, int)):
    space = {}
    lines = text.strip().splitlines()
    start = None
    end = None
    size = (len(lines[0]), len(lines))
    for y in range(len(lines)):
        for x in range(len(lines[0])):
            pos = Position(x, y)
            space[pos] = lines[y][x]
            if space[pos] == 'S':
                start = pos
            if space[pos] == 'E':
                end = pos
    return space, start, end, size

def printSpace(space: Space, size: (int, int)):
    for y in range(size[1]):
        print(''.join(list(space[Position(x, y)] for x in range(size[0]))))

# Do a pathfinding. In this case there are no dead ends or options about where to move
# That means we can go from start to end and know exactly how long it takes from each point to get to the end
# The distance from the start is saved in the space
def findPath(start: Position, end: Position, space: Space) -> [Position]:
    path = [start] # positions
    space[start] = 0
    while path[-1] != end:
        for direction in DIRECTIONS:
            step = path[-1] + direction
            if space[step] != '#' and step not in path:
                path.append(step)
                space[step] = len(path) - 1
    return path

@dataclass
class Cheat:
    start: Position
    end: Position
    timeSaved: int

    def __eq__(self, other):
        return self.start == other.start and self.end == other.end

    def __hash__(self):
        return hash((self.start, self.end))

# For every step on the path look for possible cheats within cheatPicoseconds steps
# A cheat is defined by its start, end, and the amount of time saved
def findCheats(path: [Position], space: Space, cheatPicoseconds: int) -> [Cheat]:
    cheats = set()
    for step in path:
        # find all possible cheats within radius of cheatPicoseconds
        for x in range(cheatPicoseconds + 1):
            for y in range(cheatPicoseconds - x + 1):
                for quadrant in QUADRANTS:  # every vector to each quadrant
                    end = step + Position(quadrant.x * x, quadrant.y * y)
                    if end in space and space[end] != "#":
                        timeReduction = space[end] - (space[step] + x + y)
                        if timeReduction > 0:
                            cheats.add(Cheat(step, end, timeReduction))
    return cheats

def doTheThing(text: str, savingThreshold: int, cheatPicoseconds: int):
    space, start, end, size = getSpace(text)
    path = findPath(start, end, space)
    print(f'Found a path with length {len(path)} picoseconds')
    cheats = findCheats(path, space, cheatPicoseconds)
    goodCheats = [cheat for cheat in cheats if cheat.timeSaved >= savingThreshold]
    print(f'Found {len(goodCheats)} cheats worth at least {savingThreshold} picoseconds')

if __name__ == "__main__":
    # part 1
    doTheThing(example1, 50, 2)
    doTheThing(open('input.txt').read(), 100, 2)

    # part 2
    doTheThing(example1, 50, 20)
    doTheThing(open('input.txt').read(), 100, 20)
