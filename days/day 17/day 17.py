
test2 = """
Register A: 10
Register B: 0
Register C: 0

Program: 5,0,5,1,5,4
"""

test2Output = "0,1,2"

test3 = """
Register A: 2024
Register B: 0
Register C: 0

Program: 0,1,5,4,3,0
"""

test3Output = "4,2,5,6,7,7,7,7,3,1,0"

example1 = """
Register A: 729
Register B: 0
Register C: 0

Program: 0,1,5,4,3,0
"""

example1Output = "4,6,3,5,6,3,5,2,1,0"

realInput = """
Register A: 33940147
Register B: 0
Register C: 0

Program: 2,4,1,5,7,5,1,6,4,2,5,5,0,3,3,0
"""

realOutput = "2,7,6,5,6,0,2,3,1"

class Computer:
    A: int
    B: int
    C: int
    program: [int]
    pointer = 0

    def __init__(self, text: str):
        lines = text.strip().splitlines()
        self.A = int(lines[0].split(': ')[-1])
        self.B = int(lines[1].split(': ')[-1])
        self.C = int(lines[2].split(': ')[-1])
        self.program = [int(c) for c in lines[4].split(': ')[-1].split(',')]

    def run(self) -> [int]:
        output = []
        while self.pointer < len(self.program):
            result = self.tick()
            if result is not None:
                output.append(result)
        return output

    def tick(self):
        return self.instruction(self.program[self.pointer], self.program[self.pointer+1])

    def comboOperand(self, value: int) -> int:
        match value:
            case 0:
                return 0
            case 1:
                return 1
            case 2:
                return 2
            case 3:
                return 3
            case 4:
                return self.A
            case 5:
                return self.B
            case 6:
                return self.C
            case 7 | _:
                raise ValueError

    def instruction(self, instruction: int, operand: int):
        match instruction:
            case 0:
                # adv
                self.A = self.A // (2 ** self.comboOperand(operand))
                self.pointer += 2
            case 1:
                # bxl
                self.B = self.B ^ operand
                self.pointer += 2
            case 2:
                # bst
                self.B = self.comboOperand(operand) % 8
                self.pointer += 2
            case 3:
                # jnz
                if self.A != 0:
                    self.pointer = operand
                else:
                    self.pointer += 2
            case 4:
                # bxc
                self.B = self.B ^ self.C
                self.pointer += 2
            case 5:
                # out
                self.pointer += 2
                return self.comboOperand(operand) % 8
            case 6:
                # bdv
                self.B = self.A // (2 ** self.comboOperand(operand))
                self.pointer += 2
            case 7:
                # cdv
                self.C = self.A // (2 ** self.comboOperand(operand))
                self.pointer += 2
            case _:
                raise ValueError

def doTheThing(text: str, expectedOutput=None, partTwo=False, expectedRegA=None):
    computer = Computer(text)
    if not partTwo:
        outString = ','.join(str(c) for c in computer.run())
        print(f'Got output {outString}')
        if expectedOutput:
            assert outString == expectedOutput
    if partTwo:
        # the length of the output bounds the values of A possible
        # since A is only set once in each loop of the program: A = A // 8
        # A must be between 8 ** 16 - 1 and 8 ** 15 + 1
        # unfortunately, that's still about a gajillion (8 ** 15) possibilities
        # so instead, let's go step by step backwards:
        # from the back of the program, find
        # the value of A that produces the last character

        def findARegister(aSoFar: int, iteration: int) -> int:
            for a in range(8):
                candidate = aSoFar * 8 + a
                computer = Computer(text) # reset
                computer.A = candidate
                output = computer.run()
                if output == computer.program[-1-iteration:]:
                    if len(output) == len(computer.program):
                        return candidate
                    result = findARegister(candidate, iteration + 1)
                    if result is not None:
                        return result
            return None

        accumulatedARegister = findARegister(0, 0)
        print(f'found A register value {accumulatedARegister}')
        computer = Computer(text) # reset
        computer.A = accumulatedARegister
        output = computer.run()
        assert output == computer.program

def tests():
    c = Computer("""
    Register A: 0
    Register B: 0
    Register C: 9
    
    Program: 2,6
    """)
    c.tick()
    assert c.B == 1

if __name__ == "__main__":
    # examples
    tests()
    doTheThing(test2, expectedOutput=test2Output)
    doTheThing(test3, expectedOutput=test3Output)
    doTheThing(example1, expectedOutput=example1Output)

    # part 1
    doTheThing(realInput, expectedOutput=realOutput)

    # part 2
    doTheThing(realInput, partTwo=True)
