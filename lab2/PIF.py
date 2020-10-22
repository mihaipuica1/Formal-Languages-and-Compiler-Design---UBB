class PIF:

    def __init__(self):
        self.__items = {}

    def addValue(self, token, id):
        self.__items.append( (token, id) )