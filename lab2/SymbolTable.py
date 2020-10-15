class SymbolTable:

    # since i wont be organizing the symbol table, ill be using
    # an index that will keep increasing
    def __init__(self):
        self.__list = []
        self.__position = -1

    # returns the corresponding position of the value, or False if the value can't be found
    def getPosition(self, value):
        for pair in self.__list:
            if value == pair[0]:
                return pair[1]
        return False

    # for adding a new value to the symbol table, we check if it already exists
    # in this case, we return it's position
    # else we add the new pair
    def addValue(self, newValue):
        if self.getPosition(newValue):
            return self.getPosition(newValue)

        self.__position += 1
        newPair = (newValue, self.__position)
        self.__list.append(newPair)
        return self.__position - 1


