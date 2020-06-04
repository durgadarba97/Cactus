# this is file to create the "grammer" for the language. Here, we define how the the vocabulary fits together correctly.
# To do this, we have to make move from regular expressions to "Context Free Grammer"
# These objects serve as nodes in this. 

from TokenType import getType

class Expression:
    def __init__(self):
        # an expression can be a literal, unary, binary, or grouping, declaration, 
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

    def toString(self):
        print("Binary(\n"+ self.expLeft + self.operator + self.expRight + ")")

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
        self.pos = 0
        self.cursor = None
        self.getNextChar()
        # TODO build the stack
        self.ast = self.expression()

    # These set of equations build the ast stack. 
    def expression(self):
        return self.equality()
    
    def equality(self):
        equality = self.comparison()

        while(self.match("!=" , "==")):
            operator = self.cursor.lexeme
            right = self.comparison()
            equality = Binary(equality, operator, right)

        return equality

    def comparison(self):
        addition = self.addition()

        while(self.match("greater" , "greaterequal" , "less" , "lessequal")):
            operator = self.cursor.lexeme
            right = self.addition()
            addition = Binary(addition, operator, right)
        
        return addition

    def addition(self):
        multi = self.multiplication()
        while(self.match("minus", "plus")):
            operator = self.cursor.lexeme
            right = self.multiplication()
            multi = Binary(multi, operator, right)

        return multi
    
    def multiplication(self):
        un = self.unary()

        while(self.match("slash", "multiply")):
            operator = self.cursor.lexeme
            right = self.unary()
            un = Binary(un, operator, right)
        return un

    
    def unary(self):
        if (self.match("not", "minus")):            
            operator = self.cursor.lexeme          
            right = self.unary()                 
            un = Unary(operator, right)

        return self.primary()
    
    def primary(self):
        # if(self.match("false")):
        #     return Expression.Literal("false")
        # elif(self.match("true")):
        #     return Expression.Literal("true")
        # elif(self.match("null")):
        #     return Expression.Literal("null")
        
        if(self.match("false", "true", "null", "int", "string")):   
            return Literal(self.cursor.lexeme)
        
        if(self.match("(")):
            exp = self.expression()
            # TODO Throw error if parenthesis isn't closed
            return Grouping(exp)
        



    # Similar to scanner but i think I do this better. 
    def match(self, *args):
        for types in args:
            if((not self.isAtEnd()) and (self.cursor.type == types)):
                self.getNextChar()
                return True
        
        return False

    def peek(self):
        return self.tokens[self.pos]

    # gets the next character while iterating the cursor.
    def getNextChar(self):
        self.pos = self.pos + 1
        self.cursor = self.tokens[self.pos - 1]
        print("ingetnextchar " + self.cursor.type)

    def isAtEnd(self):
        if(self.tokens[self.pos] == "EOF"):
            return True
        else:
            return False

    def toString(self):
        for i in self.ast :
            if(i == None):
                print("None")
            else:
                i.toString()

    