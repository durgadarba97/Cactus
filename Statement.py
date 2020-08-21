from Environment import state

class Statement():
    pass
    
class Return(Statement):
    def __init__(self, val = None):
        self.value = val
    
    def evaluate(self):
        raise ReturnException(self.value)

class ReturnException(Exception):
    def __init__(self, val = None):
        super(ReturnException, self).__init__(val.evaluate())

        
class Declaration(Statement):
    def __init__(self, n, val):
        self.value = val
        self.name = n
        # self.state = s

    def evaluate(self):
        state.environment.setEnv(self.name, self.value.evaluate())

    def toString(self):
        print("Declaration( " + self.name + str(self.value) + ")")

class Print(Statement):
    def __init__(self, e):
        self.value = e
    
    def evaluate(self):
        print(self.value.evaluate())
    
    def toString(self):
        print("Print(" + self.value.toString() + ")")

class Block(Statement):
    def __init__(self, s):
        self.statements = s
        # self.state = st
    
    def evaluate(self):
        state.enclose()

        # return statement throws an exception that's handeled here. and raises it again
        # so it unravels properly to the function call. This is so that it handles variable
        # scoping properly.
        for i in self.statements:
            try:
                i.evaluate()
            except ReturnException as e:
                state.close()
                raise

        
        state.close()

# I feel like I should rewrite this. 
# wrapper to declare functions. 
class FunctionDeclaration(Statement):
    def __init__(self, n, p, b):
        self.name = n
        self.function = Function(p, b)

    def evaluate(self):
        state.environment.setEnv(self.name, self.function)

# works similar to primitive and block but handles Function types.
class Function(Statement):
    def __init__(self,p, b):
        self.parameters = p
        self.block = b
    
    def evaluate(self):
        self.block.evaluate()
        

class IfStatement(Statement):
    def __init__(self, cond, th, el = None):
        self.condition = cond
        self.thenbranch = th
        self.elsebranch = el
        
    def evaluate(self):
        if(self.condition.evaluate()):
            self.thenbranch.evaluate()
        elif(self.elsebranch != None):
            self.elsebranch.evaluate()

class While(Statement):
    def __init__(self, cond, s):
        self.condition = cond
        self.statements = s

    def evaluate(self):
        while(self.condition.evaluate()):
            self.statements.evaluate()

class For(Statement):
    def __init__(self, i, cond, inc, s):
        self.initial = i
        self.condition = cond
        self.increment = inc 
        self.statements = s

    # I just implemented for loops bc I couldn't figure out how to do it with the way 
    # python does for loops. I don't really like the for-each loop that python uses 
    # so the syntax is different.
    def evaluate(self):
        self.initial.evaluate()
        while(self.condition.evaluate()):
            self.statements.evaluate()
            self.increment.evaluate()
