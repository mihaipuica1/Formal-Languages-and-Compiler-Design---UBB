from tabulate import tabulate


class Parser:

    def __init__(self, grammar, outFilename, sequenceFilename):
        self.__grammar = grammar
        self.__gotoList = []
        self.__outFilename = outFilename
        self.__sequenceFilename = sequenceFilename

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
            stateAction = ""
            for item in state[1]:
                if item == "X->S.":
                    table['action'][state[0]] = "accept"
                elif item[-1] == '.' and item[0] != 'X':
                    table['action'][state[0]] = "reduce " + str(self.getReduce(item))
                elif '.' in item and item[-1] != '.':
                    table['action'][state[0]] = "shift"
                else:
                    table['action'][state[0]] = "error"
                if stateAction == "":
                    stateAction = table['action'][state[0]]
                else:
                    if stateAction != table['action'][state[0]]:
                        result = "error: there is a " + stateAction + "-" + table['action'][state[0]] + " conflict"
                        self.writeResultToFile(result)
                        return

        self.__table = table

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

    def parse(self):
        self.generateTable()
        sequence = self.readSequenceFromFile()
        result = ""
        stateIndex = 0
        alpha = ["0"]
        beta = list(sequence)
        phi = []
        for character in beta:
            if character not in self.__grammar.getTerminals():
                result = "error: " + character + " is not a terminal"
                self.writeResultToFile(result)
                return
        while True:
            if self.__table["action"][stateIndex] == "shift":
                if len(beta) == 0:
                    result = "error"
                    self.writeResultToFile(result)
                    return
                a = beta[0]
                beta = beta[1:]
                stateIndex = self.__table[a][stateIndex]
                if stateIndex != "-":
                    alpha.append(a)
                    alpha.append(str(stateIndex))
                else:
                    result = "error"
                    self.writeResultToFile(result)
                    return
            else:
                if "reduce" in self.__table["action"][stateIndex]:
                    reduceIndex = int(self.__table["action"][stateIndex].split(" ")[1])
                    production = self.__grammar.getProductions()[reduceIndex - 1]
                    lhp = production[0]
                    rhp = production[3:]
                    for i in range(0, 2 * len(rhp)):
                        alpha.pop()
                    stateIndex = self.__table[lhp][int(alpha[-1])]
                    alpha.append(lhp)
                    alpha.append(stateIndex)
                    phi.append(reduceIndex)
                else:
                    if self.__table["action"][stateIndex] == "accept":
                        result += "success\n"
                        phi.reverse()
                        result += str(phi) + "\n"
                        for productionIndex in phi:
                            result += self.__grammar.getProductions()[productionIndex - 1] + "\n"
                        self.writeResultToFile(result)
                        return
                    else:
                        result = "error"
                        self.writeResultToFile(result)
                        return

    def readSequenceFromFile(self):
        with open(self.__sequenceFilename) as file:
            return file.readline().strip()

    def writeResultToFile(self, result):
        with open(self.__outFilename, "w") as file:
            file.write(result)