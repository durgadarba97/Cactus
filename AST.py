# this is file to create the "grammer" for the language. Here, we define how the the vocabulary fits together correctly.
# To do this, we have to make move from regular expressions to "Context Free Grammer"
# These objects serve as nodes in this. 
class Expression:
    def __init__(self, e):
        # an expression can be a literal, unary, binary, or grouping.
        pass

class Literal(Expression):
    def __init__(self, l):
        self.literal = l

class Grouping(Expression):
    def __init__(self, g, e):
        self.grouping = "(" + e + ")"

class Unary(Expression):
    def __init__(self, u, e):
        self.unary = u + e

class Binary(Expression):
    def __init__(self, left, o, right):
        self.operator = o
        self.expRight = right
        self.expLeft = left

class Declaration(Expression):
    def __init__(self, val, n):
        self.value = val
        self.name = n


def test(scanner):
    scanner.toString()
    syntaxtree = AST(scanner.tokens)


# Builds the abstract syntax tree using recursive descent.


class AST:

    def __init__(self, t):
        self.tokens = t
        self.cursor = 0

        parse()

    def parse(self):
        tok = self.gettoken()
        if(tok.type == "EOF"):
            print("parsed!")

    def gettoken(self):
        return self.gettoken[cursor]

    