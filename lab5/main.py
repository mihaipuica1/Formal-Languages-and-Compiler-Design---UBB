from Parser import Parser

from Grammar import *
#TODO: tratat conflicte si code review pentru rares si pugna echipa 3 git pugna
grammar = Grammar("g2-conflict.txt")
grammar.getGrammarFromFile()
grammar.menu()

parser = Parser(grammar, "out1.txt", "seq.txt")
parser.parse()

