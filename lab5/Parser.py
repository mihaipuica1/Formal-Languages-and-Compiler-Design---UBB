class Parser:

    def __init__(self, grammar):
        self.__grammar = grammar

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
                print(state)
                for X in NUE:
                    gotoResult = self.goto(state, X, self.__grammar.getProductions())
                    if gotoResult != [] and gotoResult not in canonicalCollection:
                        canonicalCollection.append(gotoResult)
            if canonicalCollection == initialC:
                break

        return canonicalCollection