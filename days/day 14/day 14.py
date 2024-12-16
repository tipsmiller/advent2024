import copy
import pprint
from dataclasses import dataclass

from PIL import Image, ImageDraw

example1 = """
p=0,4 v=3,-3
p=6,3 v=-1,-3
p=10,3 v=-1,2
p=2,0 v=2,-1
p=0,0 v=1,3
p=3,0 v=-2,-2
p=7,6 v=-1,-3
p=3,0 v=-1,-2
p=9,3 v=2,3
p=7,3 v=-1,2
p=2,4 v=2,-3
p=9,5 v=-3,-3
"""

example2 = """
p=2,4 v=2,-3
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
        elif isinstance(other, Position):
            return Position(self.x * other.x, self.y * other.y)

    __rmul__ = __mul__

    def __truediv__(self, other):
        if isinstance(other, int):
            return Position(self.x / other, self.y / other)
        elif isinstance(other, Position):
            return Position(self.x / other.x, self.y / other.y)

    def __hash__(self):
        return hash((self.x, self.y))

@dataclass
class Robot:
    position: Position
    velocity: Position

    def step(self, space: [[str]]):
        self.position.x = (self.position.x + self.velocity.x) % (len(space[0]))
        self.position.y = (self.position.y + self.velocity.y) % (len(space))

    def placeInSpace(self, space: [[str]]):
        if space[self.position.y][self.position.x] == '.':
            space[self.position.y][self.position.x] = '1'
        else:
            space[self.position.y][self.position.x] = str(int(space[self.position.y][self.position.x]) + 1)


def getRobots(text: str) -> [Robot]:
    robots = []
    for line in text.strip().splitlines():
        parts = line.split(' ')
        parts = [part.split('=')[1].split(',') for part in parts]
        p = Position(int(parts[0][0]), int(parts[0][1]))
        v = Position(int(parts[1][0]), int(parts[1][1]))
        robots.append(Robot(p, v))
    return robots

def displayRobots(robots: [Robot], space: [[str]]):
    display = copy.deepcopy(space)
    for robot in robots:
        robot.placeInSpace(display)
    for line in display:
        print(''.join(line))
    print('')

def getQuadrantScore(robots: [Robot], space: [[str]]) -> int:
    # quads are: 0, 1
    #            2, 3
    quadX = len(space[0]) // 2
    quadY = len(space) // 2
    quadsExtents = [
        [0, quadX, 0, quadY],
        [quadX + 1, len(space[0]), 0, quadY],
        [0, quadX, quadY + 1, len(space)],
        [quadX + 1, len(space[0]), quadY + 1, len(space)],
    ]
    scores = [0, 0, 0, 0]
    for robot in robots:
        for i, quad in enumerate(quadsExtents):
            if quad[0] <= robot.position.x < quad[1] and quad[2] <= robot.position.y < quad[3]:
                scores[i] += 1
    return scores[0] * scores[1] * scores[2] * scores[3]

def doMomentSearch(robots: [Robot], space: [[str]]) -> bool:
    # try to compute moment of inertia around the central y axis
    # small moments should indicate grouping around the center (maybe a tree!)
    # moment is the sum of the moments of all the particles: sum(m*r^2)
    # conveniently, all robots are known to have a mass of 1
    moment = 0
    centerX = len(space[0]) / 2
    centerY = len(space) / 2
    for robot in robots:
        distance = (abs(robot.position.x - centerX) ** 2) ** 0.5 # abs(robot.position.x - centerX) ** 2 +
        moment += distance ** 2
    print(f'found moment {moment}')
    return moment < 200000

def doSymmetricitySearch(robots: [Robot], space: [[str]]) -> bool:
    # get vectors to the center, then add them all.
    # A low number should indicate high symmetricity about an axis
    centerX = len(space[0]) / 2
    centerY = len(space) / 2
    totalVector = Position(0, 0)
    for robot in robots:
        totalVector += Position(robot.position.x - centerX, robot.position.y - centerY)
    print(f'found total vector {totalVector}')
    return abs(totalVector.x) < 10

def doLineSearch(robots: [Robot], space: [[str]]) -> bool:
    # look for vertical lines, could be the tree trunk?
    lines = {}
    for robot in robots:
        lines.setdefault(robot.position.x, set()).add(robot.position)
    for line in lines.values():
        if len(line) > len(space) - 80:
            print(f'found line with length {len(line)}')
            return True
    return False


def getFrame(robots: [Robot], space: [[str]], frameNum: int):
    frame = Image.new('RGB', (len(space[0]), len(space)))
    draw = ImageDraw.Draw(frame)
    for robot in robots:
        draw.point((robot.position.x, robot.position.y), 'white')
    draw.text((0, 0), str(frameNum), fill='white')
    return frame

def saveAnimationFile(frames: [Image]):
    frames[0].save('anim.gif', format='GIF', append_images=frames[1:], save_all=True, duration=100, loop=0)

def doTheThing(text: str, spaceSize: (int, int), numSeconds: int, showSteps=False, searchForTree=False, makeGif=False):
    robots = getRobots(text)
    space = [['.' for col in range(spaceSize[0])] for row in range(spaceSize[1])]
    if makeGif:
        frames = []
    if showSteps:
        displayRobots(robots, space)
    for second in range(numSeconds):
        for robot in robots:
            robot.step(space)
        if showSteps:
            displayRobots(robots, space)
        if searchForTree:
            if doLineSearch(robots, space): # doMomentSearch(robots, space) and doSymmetricitySearch(robots, space):
                break
        if makeGif:
            frames.append(getFrame(robots, space, second))
        qscore = getQuadrantScore(robots, space)
        if qscore < 200000000:
            print(second)
            print(f'Quadrant score: {qscore}')
            displayRobots(robots, space)
    print(f'After {numSeconds} seconds:')
    displayRobots(robots, space)
    print(f'Quadrant score: {getQuadrantScore(robots, space)}')
    if makeGif:
        saveAnimationFile(frames)

if __name__ == "__main__":
    # examples
    doTheThing(example2, (11, 7), 5, True)
    doTheThing(example1, (11, 7), numSeconds=100)

    # full input
    doTheThing(open('input.txt').read(),  (101, 103), numSeconds=100)

    # part 2
    doTheThing(open('input.txt').read(),  (101, 103), numSeconds=10000, makeGif=True)
