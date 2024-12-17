from copy import copy
from dataclasses import dataclass
from pprint import pprint

exampleSpace1 = """
########
#..O.O.#
##@.O..#
#...O..#
#.#.O..#
#...O..#
#......#
########
"""

exampleCommands1 = """
<^^>>>vv<v>>v<<
"""

exampleTest1 = """
########
#....OO#
##.....#
#.....O#
#.#O@..#
#...O..#
#...O..#
########
"""

exampleSpace2 = """
##########
#..O..O.O#
#......O.#
#.OO..O.O#
#..O@..O.#
#O#..O...#
#O..O..O.#
#.OO.O.OO#
#....O...#
##########
"""

exampleCommands2 = """
<vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^
vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v
><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<
<<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^
^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><
^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^
>^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^
<><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>
^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>
v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^
"""

exampleTest2 = """
##########
#.O.O.OOO#
#........#
#OO......#
#OO@.....#
#O#.....O#
#O.....OO#
#O.....OO#
#OO....OO#
##########
"""

exampleTest2_2 = """
####################
##[].......[].[][]##
##[]...........[].##
##[]........[][][]##
##[]......[]....[]##
##..##......[]....##
##..[]............##
##..@......[].[][]##
##......[][]..[]..##
####################
"""

exampleSpace3= """
#######
#...#.#
#.....#
#..OO@#
#..O..#
#.....#
#######
"""

exampleCommands3 = """
<vv<<^^<<^^
"""

exampleTest3 = """
##############
##...[].##..##
##...@.[]...##
##....[]....##
##..........##
##..........##
##############
"""

exampleSpace4 = """
#######
#...#.#
#..O..#
#..O@.#
#.OO..#
#.....#
#######
"""

exampleCommands4 = """
<>vv<^^^
"""
exampleTest4 = """
##############
##....[]##..##
##...[].....##
##....[]....##
##..[].@....##
##..........##
##############
"""

exampleSpace5 = """
#######
#.....#
#.OO@.#
#.....#
#######
"""

exampleCommands5 = """
<<
"""

exampleSpace6 = """
#######
#.....#
#.O#..#
#..O@.#
#.....#
#######
"""

exampleCommands6 = """
<v<<^
"""

exampleSpace7 = """
#######
#.....#
#.#O..#
#..O@.#
#.....#
#######
"""

exampleCommands7 = """
<v<^
"""

exampleSpace8 = """
######
#....#
#.O..#
#.OO@#
#.O..#
#....#
######
"""

exampleCommands8 = """
<vv<<^
"""

exampleSpace9 = """
######
#....#
#..#.#
#....#
#.O..#
#.OO@#
#.O..#
#....#
######
"""

exampleCommands9 = """
<vv<<^^^
"""

exampleSpace10 = """
########
#......#
#OO....#
#.O....#
#.O....#
##O....#
#O..O@.#
#......#
########
"""

exampleCommands10 = """
<^^<<>^^^<v
"""

exampleSpace11 = """
########
#...O.O#
#....O.#
#..@O.O#
#....O.#
#......#
########
"""

exampleCommands11 = """
>>vv>>^^
"""

exampleTest11 = """
################
##......[][][]##
##.......[]...##
##........[][]##
##........@...##
##............##
################
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

    def gpsCoord(self):
        return 100 * self.y + self.x

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

def getSpace(text: str, partTwo, test=False) -> ({Position: str}, {str}):
    lines = text.strip().splitlines()
    if partTwo and not test:
        newLines = []
        for line in lines:
            newLine = ''
            for c in line:
                match c:
                    case '#':
                        newLine += '##'
                    case 'O':
                        newLine += '[]'
                    case '.':
                        newLine += '..'
                    case '@':
                        newLine += '@.'
            newLines.append(newLine)
        lines = newLines
    space = {}
    values = set()
    robotPosition = None
    xSize, ySize = len(lines[0]), len(lines)
    for y in range(ySize):
        for x in range(xSize):
            value = lines[y][x]
            space[Position(x, y)] = value
            values.add(value)
            if value == '@':
                robotPosition = Position(x, y)
    return space, values, robotPosition, (xSize, ySize)

def doCommand(command: str, space: Space, robotPosition: Position, partTwo):
    direction = COMMANDS[command]
    # check values in the direction of the command
    # if there's no open spaces before a wall, nothing moves
    if not partTwo or direction in [COMMANDS['<'], COMMANDS['>']]:
        cursor = robotPosition
        thingsToShift = [robotPosition]
        while space[cursor] != '#':
            nextPosition = cursor + direction
            if space[nextPosition] == '.':
                # shift everything by direction
                for thing in reversed(thingsToShift):
                    space[thing + direction] = space[thing]
                space[robotPosition] = '.'
                # mutate robot position
                robotPosition.x += direction.x
                robotPosition.y += direction.y
                break
            else:
                thingsToShift.append(nextPosition)
            cursor = nextPosition
    elif partTwo:
        # boxes are two spaces wide "[]" and must be kept in one piece
        # this means that a box can push two boxes behind it
        # find all the boxes that are affected by the move with a search
        # then determine if they can all move by checking for walls in the direction of movement
        boxes = {robotPosition: '@'}
        while True:
            newBoxes = copy(boxes)
            for boxPosition in boxes:
                if space[boxPosition + direction] == '#':
                    return False
                if  space[boxPosition + direction] == '[':
                    newBoxes[boxPosition + direction] = '['
                    newBoxes[boxPosition + direction + COMMANDS['>']] = ']'
                if  space[boxPosition + direction] == ']':
                    newBoxes[boxPosition + direction] = ']'
                    newBoxes[boxPosition + direction + COMMANDS['<']] = '['
            if newBoxes == boxes:
                # no changes since last iteration
                break
            boxes = newBoxes

        # remove all the boxes from the space and replace with "."
        # move all the boxes in the direction
        # place them all back in the space
        movedBoxes = {}
        for box in boxes:
            space[box] = '.'
            movedBoxes[box + direction] = boxes[box]
        for box in movedBoxes:
            space[box] = movedBoxes[box]
        # mutate robot position
        robotPosition.x += direction.x
        robotPosition.y += direction.y

def printSpace(space: Space, size: (int, int)):
    out = []
    for y in range(size[1]):
        out.append(''.join(list(space[Position(x, y)] for x in range(size[0]))))
    pprint(out)

def doTheThing(spaceText: str, commandText: str, printProgress=False, test: str=None, partTwo=False, interactive=False, expectedScore=None):
    space, values, robotPosition, size = getSpace(spaceText, partTwo)
    commands = []
    for line in commandText.strip().splitlines():
        commands.extend(list(line))
    if not interactive:
        for command in commands:
            if printProgress:
                print(f'Doing command {command}')
            doCommand(command, space, robotPosition, partTwo)
            if printProgress:
                printSpace(space, size)
    elif interactive:
        command = input('next command')
        while command in commands:
            doCommand(command, space, robotPosition, partTwo)
            if printProgress:
                printSpace(space, size)
            commands.append(command)
            command = input('next command')
    if test:
        testSpace, _, _, _ = getSpace(test, partTwo, test=True)
        assert space == testSpace
    score = sum(p.gpsCoord() for p in space if space[p] in ["O", "["])
    print(f'sum of coords: {score}')
    if expectedScore:
        assert score == expectedScore

if __name__ == "__main__":
    # examples
    doTheThing(exampleSpace1, exampleCommands1, test=exampleTest1, expectedScore=2028)
    doTheThing(exampleSpace2, exampleCommands2, test=exampleTest2, expectedScore=10092)

    # part 1
    doTheThing(open('space.txt').read(), open('commands.txt').read())

    #part 2 examples
    doTheThing(exampleSpace4, exampleCommands4, partTwo=True, test=exampleTest4)
    doTheThing(exampleSpace3, exampleCommands3, partTwo=True, test=exampleTest3)
    doTheThing(exampleSpace2, exampleCommands2, partTwo=True, test=exampleTest2_2)
    doTheThing(exampleSpace5, exampleCommands5, partTwo=True, expectedScore=406)
    doTheThing(exampleSpace6, exampleCommands6, partTwo=True, expectedScore=509)
    doTheThing(exampleSpace7, exampleCommands7, partTwo=True, expectedScore=511)
    doTheThing(exampleSpace8, exampleCommands8, partTwo=True, expectedScore=816)
    doTheThing(exampleSpace9, exampleCommands9, partTwo=True, expectedScore=1216)
    doTheThing(exampleSpace10, exampleCommands10, partTwo=True, expectedScore=2827)
    doTheThing(exampleSpace11, exampleCommands11, test=exampleTest11, partTwo=True)

    # part 2
    doTheThing(open('space.txt').read(), open('commands.txt').read(), partTwo=True)
