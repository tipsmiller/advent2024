import pprint

example = """
125 17
"""

def iterateStones(text: str, iterations: int):
    stones = text.strip().split(' ')
    stoneCounts = {}
    for stone in stones:
        stoneCounts.setdefault(stone, 0)
        stoneCounts[stone] += 1
    for i in range(iterations):
        newStoneCounts = {}
        for stone, count in stoneCounts.items():
            if stone == '0':
                newStoneCounts.setdefault('1', 0)
                newStoneCounts['1'] += count
            elif len(stone) % 2 == 0:
                newStoneCounts.setdefault(stone[:len(stone)//2], 0)
                newStoneCounts[stone[:len(stone)//2]] += count
                newStoneCounts.setdefault(str(int(stone[len(stone)//2:])), 0)
                newStoneCounts[str(int(stone[len(stone)//2:]))] += count
            else:
                newStoneCounts.setdefault(str(int(stone) * 2024), 0)
                newStoneCounts[str(int(stone) * 2024)] += count
        stoneCounts = newStoneCounts
        print(f'iteration {i+1}, stones {sum(stoneCounts.values())}')
    print(f'final stone count: {sum(stoneCounts.values())}')

if __name__ == "__main__":
    # part 1 example
    iterateStones(example, 25)

    # part 1
    iterateStones(open('input.txt').read(), 25)

    # part 2 example
    # doPart2(example)

    # part 2 example
    iterateStones(open('input.txt').read(), 75)
