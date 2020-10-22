import re

# is a sequence of letters and digits,
# the first char being a letter
def isIdentifier(token):
    return re.match("^[a-zA-z]([a-zA-Z]|[0-9])*$", token) is not None


# can be an integer, a char between ' ' or a string between " "
def isConstant(token):
    return re.match("^(0|[1-9]+)|[0-9]$", token) is not None or \
           re.match("^\'[a-zA-z]\'$", token) is not None or \
           re.match("^\".\"$")

# checks if it is a separator
def isSeparator(token):
    return re.match("^[()\[\]{};: ]$", token) is not None


# checks if it is an operator
def isOperator(token):
    return re.match("")


# checks if it is a reserved word
def isReservedWord(token):
    return re.match("")

def tokenizeLine(line):
    charIndex = 0
    currentToken = ''

    while charIndex < len(line):
        if line[charIndex] !=