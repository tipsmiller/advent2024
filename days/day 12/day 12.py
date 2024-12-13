from dataclasses import dataclass

example1 = """
AAAA
BBCD
BBCC
EEEC
"""

example2 = """
OOOOO
OXOXO
OOOOO
OXOXO
OOOOO
"""

example3 = """
RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE
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

    def getNumFences(self, space: 'Space') -> int:
        fences = 0
        for direction in DIRECTIONS:
            neighbor = self + direction
            if neighbor not in space:
                fences += 1
            elif space[neighbor] != space[self]:
                fences += 1
        return fences

    def findNeighbors(self, space: 'Space', neighbors: {'Position'}) -> {'Position'}:
        for direction in DIRECTIONS:
            neighbor = self + direction
            if neighbor in space and space[neighbor] == space[self] and neighbor not in neighbors:
                neighbors.add(neighbor)
                neighbor.findNeighbors(space, neighbors)
        return neighbors

@dataclass
class State:
    pos: Position
    direction: Position

    def __eq__(self, other):
        return self.pos == other.pos and self.direction == other.direction

    def __hash__(self):
        return hash((self.pos, self.direction))

Space = {Position: str}

DIRECTIONS = [
    Position(1, 0),  # right
    Position(0, 1),  # down
    Position(-1, 0), # left
    Position(0, -1), # up
]

class Region:
    positions: {Position}
    start: Position
    xmax: int
    xmin: int
    ymax: int
    ymin: int

    def __init__(self, space: Space, start: Position):
        self.start = start
        self.positions = {start}
        start.findNeighbors(space, self.positions)
        self.xmax = start.x
        self.ymax = start.y
        self.xmin = start.x
        self.ymin = start.y
        for pos in self.positions:
            self.xmax = max(self.xmax, pos.x)
            self.ymax = max(self.ymax, pos.y)
            self.xmin = min(self.xmin, pos.x)
            self.ymin = min(self.ymin, pos.y)

    def area(self) -> int:
        return len(self.positions)

    def perimeter(self, space: Space) -> int:
        return sum(p.getNumFences(space) for p in self.positions)

    def sides(self, space: Space) -> int:
        # Go by rows and columns. Count the contiguous Positions that have a different neighbor. That's a side.
        sides = 0
        for direction in DIRECTIONS:
            if direction.x == 0:
                r = range(self.ymin, self.ymax + 1)
            else:
                r = range(self.xmin, self.xmax + 1)
            for row in r:  # or column
                fences = ''
                if direction.x == 0:
                    positionsToCheck = sorted([p for p in self.positions if p.y == row], key=lambda p: p.x)
                else:
                    positionsToCheck = sorted([p for p in self.positions if p.x == row], key=lambda p: p.y)
                lastPos = None
                for pos in positionsToCheck:
                    if lastPos and (abs((pos-lastPos).x) > 1 or abs((pos-lastPos).y) > 1):
                        fences += ' '
                    neighbor = pos + direction
                    if space.get(neighbor, '.') == space[pos]:
                        fences += ' '
                    else:
                        fences += '-'
                    lastPos = pos
                print(f'for direction {direction}, row {row}: fences "{fences}"')
                sides += len([f for f in fences.split(' ') if f != ''])
        assert sides % 2 == 0
        return sides

def getSpace(text: str) -> ({Position: str}, {str}):
    lines = text.strip().splitlines()
    space = {}
    values = set()
    for y in range(len(lines)):
        for x in range(len(lines[y])):
            space[Position(x, y)] = lines[y][x]
            values.add(lines[y][x])
    return space, values

def getFences(text: str):
    space, values = getSpace(text)
    # regions are sets of Positions which are all adjacent and have the same value
    # there are multiple regions of a value
    regions = dict((v, []) for v in values)
    totalPricePart1 = 0
    totalPricePart2 = 0
    for pos in space:
        value = space[pos]
        if len(regions[value]) == 0 or not any(pos in r.positions for r in regions[value]):
            region = Region(space, pos)
            regions[value].append(region)
            area = region.area()
            perimeter = region.perimeter(space)
            sides = region.sides(space)
            print(f'Found a region for value {value} with area {area}, perimeter {perimeter}, and sides {sides}')
            totalPricePart1 += area * perimeter
            totalPricePart2 += area * sides
    print(f'total price, part 1: {totalPricePart1}, part 2: {totalPricePart2}\n')

if __name__ == "__main__":
    # examples
    getFences(example1)
    getFences(example2)
    getFences(example3)

    # full input
    getFences(open('input.txt').read())