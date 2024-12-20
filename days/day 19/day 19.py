example1 = """
r, wr, b, g, bwu, rb, gb, br

brwrr
bggr
gbbr
rrbgbr
ubwu
bwurrg
brgr
bbrgwb
"""

def parseTowels(text: str) -> ({str: bool}, [str]):
    lines = text.strip().splitlines()
    patterns = dict((p, True) for p in lines[0].split(', '))
    desiredDesigns = lines[2:]
    return patterns, desiredDesigns

def findCombos(patterns: {str: bool}, design: str, cache: {str: int}) -> int:
    if design in cache:
        return cache[design]
    count = 0
    if len(design) == 0:
        return 1
    for pattern in patterns:
        if design.startswith(pattern):
            count += findCombos(patterns, design[len(pattern):], cache)
    cache[design] = count
    return count

def doTheThing(text: str):
    patterns, desiredDesigns = parseTowels(text)
    print(f'Loaded {len(patterns)} patterns and {len(desiredDesigns)} desired designs')
    possibleDesigns = []
    for design in desiredDesigns:
        validCombos = findCombos(patterns, design, {})
        if validCombos > 0:
            print(f'design {design} is possible with {validCombos} combos')
            possibleDesigns.append(validCombos)
        else:
            print(f'design {design} is NOT possible')
    print(f'Found {len(possibleDesigns)} possible designs with total combos {sum(possibleDesigns)}')

if __name__ == "__main__":
    # example
    doTheThing(example1)

    # part 1
    doTheThing(open('input.txt').read())
