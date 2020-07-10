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