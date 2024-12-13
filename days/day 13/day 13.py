from dataclasses import dataclass

example = """
Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=7870, Y=6450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=18641, Y=10279
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
class Machine:
    aButton: Position  # pressing costs 3
    bButton: Position  # pressing costs 1
    prize: Position

    def getPossiblePresses(self) -> (int, int):
        a = ((self.prize.x*self.bButton.y - self.prize.y*self.bButton.x) /
             (self.bButton.y * self.aButton.x - self.aButton.y * self.bButton.x))
        b = (self.prize.y - a * self.aButton.y) / self.bButton.y
        if not int(a) == a and int(b) == b:
            return 0, 0
        a = int(a)
        b = int(b)
        if not self.prize == a * self.aButton + b * self.bButton:
            return 0, 0
        return a, b

def getMachines(text: str, partTwo: bool) -> [Machine]:
    machines = []
    a = b = p = None
    for line in text.strip().splitlines():
        if line.startswith('Button A'):
            parts = line.split(', ')
            a = Position(int(parts[0].split('+')[-1]), int(parts[1].split('+')[-1]))
        if line.startswith('Button B'):
            parts = line.split(', ')
            b = Position(int(parts[0].split('+')[-1]), int(parts[1].split('+')[-1]))
        if line.startswith('Prize'):
            parts = line.split(', ')
            p = Position(int(parts[0].split('=')[-1]), int(parts[1].split('=')[-1]))
            if partTwo:
                p.x += 10000000000000
                p.y += 10000000000000
            machines.append(Machine(a, b, p))
    return machines

def doTheThing(text: str):
    machines = getMachines(text, False)
    print(f'got {len(machines)} machines')
    # find the lowest cost to get the prize
    # cost = aPresses * aCost + bPresses * bCost
    # the prize must be reachable
    # prize = aPresses * aButton + bPresses * bButton
    totalCost = 0
    for machine in machines:
        possiblePresses = machine.getPossiblePresses()
        score = 3 * possiblePresses[0] + possiblePresses[1]
        # print(f'with machine {machine} got possible presses {possiblePresses}, score {score}')
        totalCost += score
    print(f'total cost part 1: {totalCost}')

    machines = getMachines(text, True)
    totalCost = 0
    for machine in machines:
        possiblePresses = machine.getPossiblePresses()
        score = 3 * possiblePresses[0] + possiblePresses[1]
        # print(f'with machine {machine} got possible presses {possiblePresses}, score {score}')
        totalCost += score
    print(f'total cost part 2: {totalCost}')

if __name__ == "__main__":
    # examples
    doTheThing(example)

    # full input
    doTheThing(open('input.txt').read())