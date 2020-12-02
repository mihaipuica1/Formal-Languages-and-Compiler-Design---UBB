from Parser import Parser

from Grammar import *

grammar = Grammar("grammar.in")
grammar.getGrammarFromFile()
grammar.menu()

parser = Parser(grammar)
parser.parse()

