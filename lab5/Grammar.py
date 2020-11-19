class Grammar:
    def __init__(self, fileName):
        # nonTerminals - the set of nonTerminals in the grammar
        # terminals - the set of terminals in the grammar
        # startSymbol - the starting symbol of the grammar
        # productions - the set of productions
        self.__nonTerminals = None
        self.__terminals = None
        self.__startSymbol = None
        self.__productions = []
        self.__fileName = fileName

    def getGrammarFromFile(self):
        with open(self.__fileName) as file:
            # the first strip() gets rid of the newline at the end of the line
            self.__nonTerminals = file.readline().strip()
            self.__terminals = file.readline().strip()
            self.__startSymbol = file.readline().strip()

            for line in file:
                production = line.strip().replace(' ', '').split("->")
                self.__productions.append(production)

    def menu(self):
        print("1. Print the set of non-terminals")
        print("2. Print the set of terminals")
        print("3. Print the starting symbol")
        print("4. Print the productions")
        print("5. Print the productions for a given non-terminal")
        while True:
            menuCommand = input()
            if menuCommand == "1":
                print("The non-terminals set is: " + str(self.__nonTerminals))
            elif menuCommand == "2":
                print("The terminals set is: " + str(self.__terminals))
            elif menuCommand == "3":
                print("The starting symbol is: " + str(self.__startSymbol))
            elif menuCommand == "4":
                print("The productions are:")
                for production in self.__productions:
                    printedProduction = production[0] + " -> " + production[1]
                    print(printedProduction)
            elif menuCommand == "5":
                givenNonTerminal = input("Input the non-terminal: ")
                print(givenNonTerminal)
                productionsToPrint = self.getProductionsForNonTerminal(givenNonTerminal)
                print("The productions for the " + givenNonTerminal + " non-terminal are:")
                for production in productionsToPrint:
                    printedProduction = production[0] + " -> " + production[1]
                    print(printedProduction)

    def getNonTerminals(self):
        return self.__nonTerminals

    def getTerminals(self):
        return self.__terminals

    def getStartSymbol(self):
        return self.__startSymbol

    def getProductions(self):
        return self.__productions

    def getProductionsForNonTerminal(self, givenNonTerminal):
        productionsForNonTerminal = []
        for production in self.__productions:
            if production[0] == givenNonTerminal:
                productionsForNonTerminal.append(production)
        return productionsForNonTerminal
