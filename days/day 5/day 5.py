exampleRules = """47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13"""

exampleUpdates = """75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47"""

import pprint

def getRules(input: str) -> dict[int, [int]]:
    lines = input.splitlines()
    pairs = [[int(pageNum) for pageNum in line.split('|')] for line in lines]
    rules = {}
    for rule in pairs:
        rules.setdefault(rule[0], []).append(rule[1])
    print(f'parsed {len(rules)} rules')
    pprint.pprint(rules)
    return rules

def getUpdatePages(input: str) -> [[int]]:
    lines = input.splitlines()
    pages = [[int(pageNum) for pageNum in line.split(',')] for line in lines]
    print(f'parsed {len(pages)} updates')
    pprint.pprint(pages)
    return pages

def testUpdatePages(rules: dict[int, [int]], update: [int]) -> bool:
    for page in update:
        if page in rules:
            for check in rules[page]:
                if check in update:
                    if update.index(check) < update.index(page):
                        return False
    return True

def sumMedians(updates: [[int]]) -> int:
    return sum(update[int(len(update)/2)] for update in updates)

def runPart1(rulesInput: str, updatesInput: str):
    rules = getRules(rulesInput)
    updatePages = getUpdatePages(updatesInput)
    correctUpdates = []
    for update in updatePages:
        if testUpdatePages(rules, update):
            correctUpdates.append(update)
    print(f'found {len(correctUpdates)} correct updates')
    pprint.pprint(correctUpdates)
    print(f'score: {sumMedians(correctUpdates)}')

def correctUpdate(rules: dict[int, [int]], update: [int]) -> [int]:
    newUpdate = []
    for page in update:
        insertIndex = 0
        test = newUpdate[:insertIndex] + [page] + newUpdate[insertIndex:]
        while not testUpdatePages(rules, test):
            insertIndex += 1
            test = newUpdate[:insertIndex] + [page] + newUpdate[insertIndex:]
        newUpdate = test

    return newUpdate

def runPart2(rulesInput: str, updatesInput: str):
    rules = getRules(rulesInput)
    updatePages = getUpdatePages(updatesInput)
    incorrectUpdates = []
    for update in updatePages:
        if not testUpdatePages(rules, update):
            incorrectUpdates.append(update)
    print(f'found {len(incorrectUpdates)} incorrect updates')
    pprint.pprint(incorrectUpdates)
    correctedUpdates = [correctUpdate(rules, update) for update in incorrectUpdates]
    print(f'corrected updates:')
    pprint.pprint(correctedUpdates)
    print(f'score: {sumMedians(correctedUpdates)}')

if __name__ == "__main__":
    # part 1 examples
    runPart1(exampleRules, exampleUpdates)

    # part 1
    runPart1(open('inputRules.txt').read(), open('inputUpdates.txt').read())

    # part 2 examples
    runPart2(exampleRules, exampleUpdates)

    # part 2
    runPart2(open('inputRules.txt').read(), open('inputUpdates.txt').read())
