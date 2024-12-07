example = """
190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20
"""

def parseInput(input: str) -> [[int]]:
    lines = input.strip().splitlines()
    equations = []
    for line in lines:
        parts = [line.split(':')[0]]
        parts += line.split(': ')[1].split(' ')
        parts = [int(part) for part in parts]
        equations.append(parts)
    print(f'parsed {len(equations)} equations')
    return equations

def isValidEquation(targetValue: int, parts: [int], operators: [str]) -> bool:
    valid = False
    for operator in operators:
        match operator:
            case '*':
                leftVal = parts[0] * parts[1]
            case '+':
                leftVal = parts[0] + parts[1]
            case '||':
                leftVal = int(str(parts[0]) + str(parts[1]))
            case _:
                raise ValueError(f'invalid operator: {operator}')
        if leftVal > targetValue:
            continue
        rightVals = parts[2:]
        if len(rightVals) == 0:
            valid = valid or leftVal == targetValue
            if valid:
                return True
        else:
            valid = valid or isValidEquation(targetValue, [leftVal] + rightVals, operators)
            if valid:
                return True
    return valid

def sumValidEquations(equations: [[int]], operators):
    score = 0
    for equation in equations:
        targetValue = equation[0]
        if isValidEquation(targetValue, equation[1:], operators):
            score += targetValue
    print(f'Score: {score}')

if __name__ == "__main__":
    # part 1 example
    sumValidEquations(parseInput(example), ['*', '+'])

    # part 1
    sumValidEquations(parseInput(open('input.txt').read()), ['*', '+'])

    # part 2 example
    sumValidEquations(parseInput(example), ['||', '*', '+'])

    # part 2
    sumValidEquations(parseInput(open('input.txt').read()), ['||', '*', '+'])
