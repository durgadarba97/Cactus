# this is file to create the "grammer" for the language. Here, we define how the the vocabulary fits together correctly.
# To do this, we have to make move from regular expressions to "Context Free Grammer"
# These objects serve as nodes in this. 

from TokenType import getType
from Expression import *
from Statement import *
from Environment import *

# Builds the abstract syntax tree using recursive descent.
# TODO newline characters break the code.
class AST:

    def __init__(self, t):
        self.tokens = t
        self.pos = 0
        self.cursor = None
        self.state = State()

        # There's an issue with the way things are being parsed. Starts at position 1 instead of 0
        self.getNextChar()
        self.ast = []
        self.program()
        
        # evaluates the AST
        print("\nAST result==========>")
        for i in self.ast:
            eval = i.evaluate()

        # To String is broken for some reason. 
        # self.ast.toString()

    # program = statement + end of line character + end of file
    def program(self):
        while(not self.isAtEnd()):
            # a line can either be a variable declaration or a statement.
            self.getNextChar()

            if(self.match("identifier")):
                stmt = self.declaration()
            else:
                stmt = self.statement()

            # handles multiple newline characters at a time. 
            if(stmt is not None):
                self.ast.append(stmt)
            
            print("HERE==============")

            # this is a weird design thing.
            #  We shouldn't have to check if it's end life bc the while loops does that.
            # this solves the issue of throwing errors bc EOF cant end in new line.
            # TODO
            if(not self.match("newline") and not self.isAtEnd()):
                print("Error:\tExpected end of line")

    def declaration(self):
        varname = self.cursor.lexeme
        self.getNextChar()
        if(self.match("equal")):
            self.getNextChar()
            d = Declaration(self.state, varname, self.expression())

            return d

        
    # A single line is either a print statement or an expression.
    # This will change when we add variables
    def statement(self):
        if(self.match("print")):
            self.getNextChar()
            return Print(self.expression())
        else:
            # self.getNextChar()
            return self.expression()

    # These set of equations build the ast stack. 
    def expression(self):
        return self.equality()
    
    def equality(self):
        comp = self.comparison()

        while(self.match("notequal" , "equalequal")):
            operator = self.cursor.lexeme
            self.getNextChar()
            right = self.comparison()
            comp = Binary(comp, operator, right)

        return comp

    def comparison(self):
        addition = self.addition()

        while(self.match("greater" , "greaterequal" , "less" , "lessequal")):
            operator = self.cursor.lexeme
            self.getNextChar()
            right = self.addition()
            addition = Binary(addition, operator, right)
        
        return addition

    def addition(self):
        multi = self.multiplication()
        while(self.match("minus", "plus")):
            operator = self.cursor.lexeme
            self.getNextChar()
            right = self.multiplication()
            multi = Binary(multi, operator, right)

        return multi
    
    def multiplication(self):
        un = self.unary()

        while(self.match("divide", "multiply")):
            operator = self.cursor.lexeme
            self.getNextChar()
            right = self.unary()
            un = Binary(un, operator, right)

        return un

    
    def unary(self):
        if (self.match("not", "minus")):            
            operator = self.cursor.lexeme   
            self.getNextChar()
            # This allows things like ---2 to be valid. Change this in the future. 
            # Leaving this in here because the book does this.    
            right = self.unary()                 
            return Unary(operator, right)

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
            self.getNextChar()
            return lit
        
        if(self.match("leftparenthesis")):
            self.getNextChar()
            exp = self.expression()

            # The next token has to be a ). 
            if(self.cursor.type == "rightparenthesis"):
                self.getNextChar()
            else:
                print("Error:\topen parathensis error!")
            return Grouping(exp)

        if(self.match("identifier")):
            var = self.cursor.lexeme
            self.getNextChar()
            return Variable(self.state, var)

        
                

    # Similar to scanner but i think I do this better. 
    def match(self, *args):
        for types in args:
            if((not self.isAtEnd()) and (self.cursor.type == types)):
                # The issue is that if we increment the character before we create the object, 
                # the wrong lexeme will get passed in. In the book, they call the previous, but I chose to do it differently.
                # self.getNextChar()
                return True
        
        return False

    def peek(self):
        return self.tokens[self.pos]

    # gets the next character while iterating the cursor.
    def getNextChar(self):
        self.pos = self.pos + 1
        self.cursor = self.tokens[self.pos - 1]
        print("ingetnextchar " + self.cursor.toString())

    def isAtEnd(self):
        if(self.cursor.type == "EOF"):
            return True
        else:
            return False

    def toString(self):
        self.ast.toString()

    