from Environment import state
from Statement import ReturnException
from Error import *
class Expression():
    def __init__(self):
        # an expression can be a literal, unary, binary, or grouping, declaration, 
        # map that defines the variables.
        pass

class Literal(Expression):
    def __init__(self, l):
        self.literal = l

    def evaluate(self):
        if(self.literal == "true"):
            return True
        elif(self.literal == "false"):
            return False
        else:
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
        elif(self.operator == "or"):
            return (self.expLeft.evaluate() or self.expRight.evaluate())
        elif(self.operator == "and"):
            return (self.expLeft.evaluate() and self.expRight.evaluate())          

    def toString(self):
        if(self.expLeft != None and self.operator != None and self.expRight != None):
            print("Binary(\n"+ self.expLeft.toString() + self.operator + self.expRight.toString() + "\n)")
        else:
            print("HERE")

# the state for a variable should just be it at a given point. 
class Variable(Expression):
    def __init__(self, n, l):
        self.name = n
        self.line = l
    
    def evaluate(self):
        try:
            return state.environment.getEnv(self.name)
        except UndeclaredVariableException as e:
            e.setError("Use of variable, \"" + self.name + "\", before assignment", self.line)
            raise


class FunctionCall(Expression):
    def __init__(self, n, params, l):
        self.name = n
        self.parameters = params
        self.line = l
    
    def evaluate(self):
        try:
            decl = state.environment.getEnv(self.name)
        except UndeclaredVariableException as e:
            e.setError("Function called before assignment", self.line)
            raise
        state.enclose()

        # TODO check to make sure decl is a Function type.

        # check arity of function.
        if(len(decl.parameters) != len(self.parameters)):
            e = ArgumentMismatchException()
            e.setError("Incorrect number of arguments in function call", self.line)
            raise e

        # initialize the parameters
        for i in range(len(self.parameters)):
            state.environment.setEnv(decl.parameters[i].name, self.parameters[i].evaluate())
        
        try:
            decl.evaluate()
        except ReturnException as e:
            state.close()
            return e.args[0]
        state.close()