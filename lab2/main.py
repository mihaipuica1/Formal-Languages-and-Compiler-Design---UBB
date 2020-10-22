from SymbolTable import SymbolTable
from PIF import PIF
from Scanner import *

pif = PIF()
SymbolTableIdentifiers = SymbolTable()
SymbolTableConstants = SymbolTable()

fileName = input("file name")

with open(fileName, 'r') as file:
    for line in file:
        tokenList = tokenizeLine(line)
        for token in tokenList:
            if isSeparator(token) or isOperator(token) or isReservedWord(token):
                pif.add(token, -1)
            elif isIdentifier(token):
                identifierId = SymbolTableIdentifiers.addValue(token)
                pif.addValue(token, identifierId)
            elif isConstant(token):
                constantId = SymbolTableConstants.addValue(token);
                pif.addValue(token, constantId)
            else:
                print("Lexical error")
