# this is file to create the "grammer" for the language. Here, we define how the the vocabulary fits together correctly.
# To do this, we have to make move from regular expressions to "Context Free Grammer"
# These objects serve as nodes in this. 

from TokenType import getType

class Expression:
    def __init__(self):
        # an expression can be a literal, unary, binary, or grouping, declaration, 
        # map that defines the variables.
        self.environment = {}

    def define(self, name, value):
        self.environment[name] = value
    
    def evaluate(self):
        return self.environment[name]
        
    def toString(self):
        pass

class Literal(Expression):
    def __init__(self, l):
        self.literal = l

    def evaluate(self):
        return self.literal

    def toString(self):
        if(self.literal == "\n"):
            print("this is a newline")
        print("Literal(" + self.literal + ")")
        return self.literal

class Grouping(Expression):
    def __init__(self, e):
        self.grouping = e
    
    def evaluate(self):
        return self.grouping.evaluate()

    def toString(self):
        print("Grouping(\n" + self.grouping.toString() + "\n)")
        return self.grouping.toString()

class Unary(Expression):
    def __init__(self, u, e):
        self.unary = u
        self.expression = e

    def evaluate(self):
        if(self.unary == "!"):
            return not self.expression.evaluate()
        elif(self.unary == "-"):
            return "-" + self.expression.evaluate() 
        

    def toString(self):
        print("Unary(" + self.unary + self.expression.toString() + ")")
        return self.unary + self.expression.toString()

class Binary(Expression):
    def __init__(self, left, o, right):
        self.operator = o
        self.expRight = right
        self.expLeft = left

    def evaluate(self):
        if(self.operator == "+"):
            return int(self.expLeft.evaluate()) + int(self.expRight.evaluate())
        elif(self.operator == "-"):
            return int(self.expLeft.evaluate()) - int(self.expRight.evaluate())
        elif(self.operator == "/"):
            return int(self.expLeft.evaluate()) / int(self.expRight.evaluate())
        elif(self.operator == "*"):
            return int(self.expLeft.evaluate()) * int(self.expRight.evaluate())
        
        # Evaluate comparisons
        elif(self.operator == "<"):
            return (self.expLeft.evaluate() < self.expRight.evaluate())
        elif(self.operator == ">"):
            return (self.expLeft.evaluate() > self.expRight.evaluate())
        elif(self.operator == "<="):
            return (self.expLeft.evaluate() <= self.expRight.evaluate())
        elif(self.operator == ">="):
            return (self.expLeft.evaluate() >= self.expRight.evaluate())
        elif(self.operator == "=="):
            return (self.expLeft.evaluate() == self.expRight.evaluate())
        elif(self.operator == "!="):
            return (self.expLeft.evaluate() != self.expRight.evaluate())
        

    def toString(self):
        if(self.expLeft != None and self.operator != None and self.expRight != None):
            print("Binary(\n"+ self.expLeft.toString() + self.operator + self.expRight.toString() + "\n)")
        else:
            print("HERE")

class Declaration(Expression):
    def __init__(self, n, val):
        self.value = val
        self.name = n
        self.define(self.name, self.value)
    
    def define(self, n, v):
        pass

    def evaluate(self):
        pass

    def toString(self):
        print("Declaration( " + self.name + str(self.value) + ")")

class Print(Expression):
    def __init__(self, e):
        self.value = e
    
    def evaluate(self):
        print(self.value.evaluate())
    
    def toString(self):
        print("Print(" + self.value.toString() + ")")



# Builds the abstract syntax tree using recursive descent.
# TODO newline characters break the code.
class AST:

    def __init__(self, t):
        self.tokens = t
        self.pos = 0
        self.cursor = None

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
            if(self.match("identifier")):
                stmt = self.declaration()
            else:
                stmt = self.statement()

            # handles multiple newline characters at a time. 
            if(stmt is not None):
                self.ast.append(stmt)
            self.getNextChar()

            # this is a weird design thing.
            #  We shouldn't have to check if it's end life bc the while loops does that.
            # this solves the issue of throwing errors bc EOF cant end in new line.
            # TODO
            if(not self.match("newline") and not self.isAtEnd()):
                print("Expected end of line")

    def declaration(self):
        x = 10
        x + 5
        varname = self.cursor.lexeme
        self.getNextChar()
        if(self.match("equal")):
            self.getNextChar()
            return Declaration(varname, self.expression())
        # if(self.match("equal")):
            
        # else:
        #     print("expecting \"=\" in variable declaration")


        
    # A single line is either a print statement or an expression.
    # This will change when we add variables
    def statement(self):
        if(self.match("print")):
            self.getNextChar()
            return Print(self.primary())
        else:
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
                print("throw error!")
            return Grouping(exp)

        if(self.match("identifier")):
            return Declaration()

        
                

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

    