# this is file to create the "grammer" for the language. Here, we define how the the vocabulary fits together correctly.
# To do this, we have to make move from regular expressions to "Context Free Grammer"
# These objects serve as nodes in this. 

from TokenType import getType

class Expression:
    def __init__(self):
        # an expression can be a literal, unary, binary, or grouping, declaration, 
        pass

    def evaluate(self):
        pass

    def toString(self):
        pass

class Literal(Expression):
    def __init__(self, l):
        self.literal = l

    def evaluate(self):
        return self.literal

    def toString(self):
        print("Literal(" + self.literal + ")")

class Grouping(Expression):
    def __init__(self, e):
        self.grouping = e
    
    def evaluate(self):
        return self.grouping.evaluate()

    def toString(self):
        print("Grouping(\n" + self.grouping + "\n)")

class Unary(Expression):
    def __init__(self, u, e):
        self.unary = u
        self.expression = e

    def evaluate(self):
        if(self.unary == "!"):
            return not self.expression
        elif(self.unary == "-"):
            return "-" + self.expression
        

    def toString(self):
        print("Unary(" + self.unary + ")")

class Binary(Expression):
    def __init__(self, left, o, right):
        self.operator = o
        self.expRight = right
        self.expLeft = left

    def evaluate(self):
        print("here:" + self.expRight.toString() + self.expLeft.toString())
        if(self.operator == "+"):
            return self.expRight.evaluate() + self.expLeft.evaluate()
        elif(self.operator == "-"):
            return self.expRight.evaluate() - self.expLeft.evaluate()
        elif(self.operator == "/"):
            return self.expRight.evaluate() / self.expLeft.evaluate()
        elif(self.operator == "*"):
            return self.expRight.evaluate() * self.expLeft.evaluate()

    def toString(self):
        print("Binary(\n"+ self.expLeft.toString() + self.operator + self.expRight.toString() + "\n)")

class Declaration(Expression):
    def __init__(self, val, n):
        self.value = val
        self.name = n

    def toString(self):
        print("Declaration( " + self.name + str(self.value) + ")")



# Builds the abstract syntax tree using recursive descent.
class AST:

    def __init__(self, t):
        self.tokens = t
        self.pos = 0
        self.cursor = None
        self.getNextChar()

        self.ast = self.expression()
        self.ast.evaluate()
        print("after evaluate")


    # These set of equations build the ast stack. 
    def expression(self):
        return self.equality()
    
    def equality(self):
        comp = self.comparison()

        while(self.match("notequal" , "equalequal")):
            operator = self.cursor.lexeme
            right = self.comparison()
            comp = Binary(equality, operator, right)

        return comp

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

        while(self.match("divide", "multiply")):
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
            lit = Literal(self.cursor.lexeme)
            return lit
        
        if(self.match("leftparenthesis")):
            exp = self.expression()

            # The next token has to be a ). 
            if(self.cursor.type == "rightparenthesis"):
                self.getNextChar()
            else:
                print("throw error!")
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
        if(self.tokens[self.pos].type == "EOF"):
            return True
        else:
            return False

    