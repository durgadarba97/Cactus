from Environment import *
class Statement():
    pass
    
        
class Declaration(Statement):
    def __init__(self, s, n, val):
        self.value = val
        self.name = n
        self.state = s

    def evaluate(self):
        self.state.setEnv(self.name, self.value)

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
    
    def evaluate(self):
        for i in self.statements:
            i.evaluate()
        

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