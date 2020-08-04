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
        self.environment = Environment()
        
        # There's an issue with the way things are being parsed. Starts at position 1 instead of 0
        self.getNextChar()
        self.ast = []

        # self.ast.append(Declaration(self.environment, "whoami", Literal("Hello, welcome to Cactus!")))

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

            stmt = self.line()

            # handles multiple newline characters at a time. 
            if(stmt is not None):
                self.ast.append(stmt)

            # this is a weird design thing.
            #  We shouldn't have to check if it's end of file bc the while loops does that.
            # this solves the issue of throwing errors bc EOF cant end in new line.
            # TODO
            if(not self.match("newline") and not self.isAtEnd()):
                print("Error:\tExpected end of line")

    def line(self):
        # If it's an identifier, it could either be a variable declaration, function declaration, or just stating a primary.
        if(self.match("identifier")):
            if(self.peek("equal")):
                stmt = self.declaration()
            else:
                stmt = self.functionCall()

        elif(self.match("leftbrace")):
            stmt = self.block()
        elif(self.match("if")):
            stmt = self.ifStatement()
        elif(self.match("while")):
            stmt = self.whileloop()
        elif(self.match("for")):
            stmt = self.forloop()
        else:
            stmt = self.statement()
        return stmt

    # Handles { } TODO better orgranize this. this is exactly like program()
    def block(self):
        blockstmts = []

        # Creates variable scope by saying that the block is the child of the parent block. 
        childenvironment = Environment(enclose = self.environment)
        self.environment = childenvironment
        while(not self.isAtEnd() and not self.match("rightbrace")):

            self.getNextChar()
            stmt = self.line()

            # handles multiple newline characters at a time. 
            if(stmt is not None):
                blockstmts.append(stmt)

            if(not self.match("newline") and not self.isAtEnd()):
                print("Error:\tExpected end of line")
        
        self.getNextChar()
        # resets variable scope to the parent.
        self.environment = childenvironment.enclosing
        return Block(blockstmts) 

    def declaration(self):
        varname = self.cursor.lexeme
        self.getNextChar()
        if(self.match("equal")):
            self.getNextChar()
            decl = Declaration(self.environment, varname, self.expression())
            return decl
        else:
            print("ERROR expected \"=\" after variable declaration")


        
    # A single line is either a print statement or an expression.
    # This will change when we add variables
    def statement(self):
        if(self.match("print")):
            self.getNextChar()
            return Print(self.expression())
        else:
            return self.expression()

    def whileloop(self):
        self.getNextChar()

        if(self.match("leftparenthesis")):
            self.getNextChar()
            condition = self.expression()

            if(not self.match("rightparenthesis")):
                print("missing right parenthesis")

            self.getNextChar()

            if(self.match("newline")):
                self.getNextChar()
            
            body = self.line()

            return While(condition, body)
        else:
            print("missing leftparenthesis")

    # TODO make sure none of these are null values. 
    # The book gives people the freedom to not include some of them
    # But I feel like that's too much syntactic sugar.
    def forloop(self):
        self.getNextChar()

        if(self.match("leftparenthesis")):
            self.getNextChar()
            initial = self.declaration()

            if(not self.match("comma")):
                print("missing comma seperator")
            self.getNextChar()

            condition = self.expression()
            if(not self.match("comma")):
                print("missing comma seperator")
            self.getNextChar()

            increment = self.declaration()
            if(not self.match("rightparenthesis")):
                print("missing right parenthesis")
            
            self.getNextChar()
            if(self.match("newline")):
                self.getNextChar()

            statements = self.line()
            return For(initial, condition, increment, statements)
        else:
            print("missing left parenthesis")

    def ifStatement(self):
        self.getNextChar()
        
        # maybe we can just call primary()
        if(self.match("leftparenthesis")):
            self.getNextChar()
            condition = self.expression()
            
            if(not self.match("rightparenthesis")):
                print("unclosed parenthesis")

            self.getNextChar()
            
            if(self.match("newline")):
                self.getNextChar()
                
            thenbranch = self.line()

            self.ignoreNewLines()
            
            # Hardcoded this because statements must end at newline character.
            # TODO edit the grammer here. Can be coded way cleaner. 
            if(self.peek("else")):
                self.getNextChar()

            elsebranch = None
            if(self.match("else")):
                self.getNextChar()
                
                if(self.match("newline")):
                    self.getNextChar()
                elsebranch = self.line()

            return IfStatement(condition, thenbranch, elsebranch)
        
        else:
            print("if statement must start a condition using left parenthesis")

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

    # included or in addition because in probablity or usually means add
    def addition(self):
        multi = self.multiplication()
        while(self.match("minus", "plus", "or")):
            operator = self.cursor.lexeme
            self.getNextChar()
            right = self.multiplication()
            multi = Binary(multi, operator, right)

        return multi
    
    # included and in multiplication because in probablity and usually means multiply
    def multiplication(self):
        un = self.unary()

        while(self.match("divide", "multiply", "and")):
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

        return self.functionCall()

    def functionCall(self):
        # put the identifier call at the end to avoid the bs name.name
        name = self.primary()
        
        if(self.match("leftparenthesis")):
            self.getNextChar()
            arguments = []
            while(not self.match("rightparenthesis")):
                # probably could've done this with a do while loop. this works for now.
                arguments.append(self.expression())

                while(self.match("comma") and len(arguments) <= 255):
                    self.getNextChar()
                    arguments.append(self.expression())


            # TODO Kind of an inefficient way to do this, but I can change this later. 
            if(len(arguments) and not self.match("rightparenthesis")):
                print("ERROR EXPECTED \")\"")
            else:

                # check if it's a function call or if it's a function declaration. 
                # idk if this is a good way to do it. the syntax might be confusing and too permissive,
                # but it's a fun thing to check out. Maybe rewrite tho.
                self.getNextChar()
                if(self.match("newline")):
                    if(self.peek("leftbrace")):
                        self.getNextChar()

                # move the primary call to the end to avoid the bs name.name TODO
                if(self.match("leftbrace")):
                    body = self.line()
                    return FunctionDeclaration(name.name, arguments, body, self.environment)
                
                else:
                    print("return function call")
                    return FunctionCall(name.name, arguments, self.environment)

        else:
            return name

    
    def primary(self):
        if(self.match("false", "true", "null", "int", "double", "string")): 
            typ = self.cursor.type
            lex = self.cursor.lexeme

            lit = Literal(lex)
            self.getNextChar()
            return lit
        
        # TODO the book makes it call another expression, but I think it only really needs to be a unary.
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
            # Creates a copy of the current environment
            self.getNextChar()
            return Variable(self.environment, var)

        
                

    # Similar to scanner but i think I do this better. 
    def match(self, *args):
        for types in args:
            if((not self.isAtEnd()) and (self.cursor.type == types)):
                # The issue is that if we increment the character before we create the object, 
                # the wrong lexeme will get passed in. In the book, they call the previous, but I chose to do it differently.
                # self.getNextChar()
                return True
        
        return False

    def peek(self, arg):
        if(arg == self.tokens[self.pos].type):
            return True
        else:
            return False

    def ignoreNewLines(self):
        while(self.tokens[self.pos].type == "newline"):
            self.getNextChar()

    # gets the next character while iterating the cursor.
    def getNextChar(self):
        self.pos = self.pos + 1
        self.cursor = self.tokens[self.pos - 1]

    def isAtEnd(self):
        if(self.cursor.type == "EOF"):
            return True
        else:
            return False

    def toString(self):
        self.ast.toString()

    