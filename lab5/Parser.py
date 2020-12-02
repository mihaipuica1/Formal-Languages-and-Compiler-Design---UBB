from tabulate import tabulate


class Parser:

    def __init__(self, grammar):
        self.__grammar = grammar
        self.__gotoList = []

    def closure(self, itemSet, productions):
        closureResult = list(itemSet)
        while True:
            before = list(closureResult)
            for item in closureResult:
                if item.index(".") != len(item) - 1:
                    symbolAfterDot = item[item.index(".") + 1]
                    for prod in productions:
                        if prod[0] == symbolAfterDot and prod[0:3] + "." + prod[3:] not in closureResult:
                            closureResult.append(prod[0:3] + "." + prod[3:])
            if before == closureResult:
                break
        return closureResult

    def swap(self, string, i, j):
        stringAsList = list(string)
        stringAsList[i], stringAsList[j] = stringAsList[j], stringAsList[i]
        return ''.join(stringAsList)

    def goto(self, itemSet, X, productions):
        itemsWithX = []
        for item in itemSet:
            if "." in item and item.index(".") != len(item) - 1:
                symbolAfterDot = item[item.index(".") + 1]
                if symbolAfterDot == X:
                    newItem = self.swap(item, item.index(".") + 1, item.index("."))
                    itemsWithX.append(newItem)
        self.__gotoList.append([itemSet, X, self.closure(itemsWithX, productions)])

        return self.closure(itemsWithX, productions)

    def computeCanonicalCollection(self):
        j = self.closure(["X->.S"], self.__grammar.getProductions())
        canonicalCollection = [j]
        N = set(self.__grammar.getNonTerminals())
        E = set(self.__grammar.getTerminals())
        NUE = N.union(E)

        while True:
            initialC = list(canonicalCollection)
            for state in canonicalCollection:
                for X in NUE:
                    gotoResult = self.goto(state, X, self.__grammar.getProductions())
                    if gotoResult != [] and gotoResult not in canonicalCollection:
                        canonicalCollection.append(gotoResult)
            if canonicalCollection == initialC:
                break
        return canonicalCollection

    def getReduce(self, item):
        productionIndex = 1
        for production in self.__grammar.getProductions():
            if production == item[:-1]:
                return productionIndex
            else:
                productionIndex += 1

    def generateTable(self):
        canonicalCollection = self.computeCanonicalCollection()
        for i in range(0, len(canonicalCollection)):
            canonicalCollection[i] = [i, canonicalCollection[i]]

        for state in canonicalCollection:
            print(state)

        noDuplicatesGotoList = []

        for goto in self.__gotoList:
            if goto not in noDuplicatesGotoList:
                noDuplicatesGotoList.append(goto)

        for goto in noDuplicatesGotoList:
            for state in canonicalCollection:
                if goto[0] == state[1]:
                    goto[0] = state[0]
                if goto[2] == state[1]:
                    goto[2] = state[0]
                if not goto[2]:
                    goto[2] = 'O'

        maxLength = len(canonicalCollection)
        table = {}
        table['action'] = ['-'] * maxLength
        for terminal in self.__grammar.getTerminals():
            table[terminal] = ['-'] * maxLength
        for nonTerminal in self.__grammar.getNonTerminals():
            table[nonTerminal] = ['-'] * maxLength

        for state in canonicalCollection:
            for goto in noDuplicatesGotoList:
                if goto[0] == state[0] and goto[2] != 'O':
                    table[goto[1]][state[0]] = goto[2]

        for state in canonicalCollection:
            for item in state[1]:
                if item == "X->S.":
                    table['action'][state[0]] = "accept"
                elif item[-1] == '.' and item[0] != 'X':
                    table['action'][state[0]] = "reduce " + str(self.getReduce(item))
                elif '.' in item and item[-1] != '.':
                    table['action'][state[0]] = "shift"

        tableHeaders = [" "]
        tableContent = []
        for row in table:
            tableHeaders.append(row)
        for i in range(len(canonicalCollection)):
            tableContent.append([str(i)])

        for state in canonicalCollection:
            for row in table:
                tableContent[state[0]].append(str(table[row][state[0]]))

        print(tabulate(tableContent, headers=tableHeaders))
