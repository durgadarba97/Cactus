from Error import *

class Environment:
    def __init__(self, enclose = None):  
        self.variables = {}
        self.enclosing = enclose
    
    # recursively checks if variable exists. Done like this for variable scoping
    def getEnv(self, name):
        # print(self.evironment["hello"])
        if(name in self.variables):
            return self.variables[name]
        elif(self.enclosing != None):
            return self.enclosing.getEnv(name)
        # return error TODO
        else:
            raise UndeclaredVariableException()
    
    #  Because var initialization and redeclaration are the same, this recursively check if parent
    #  environment has the variable and set it at that level. If not, creates a new variable at child.
    #  Done like this for variable scoping.s
    def setEnv(self, name, value):
        # found = self.find(name)

        # if(found != False):
        #     found.variables[name] = value
        # else:
        #     self.variables[name] = value
        
        self.variables[name] = value

        return True
        # TODO return error

    #  recursive method to find which scoping level the variable exists.
    #  Idk if this is a good design pattern, but it works from the looks of it.
    def find(self, name):
        if(name in self.variables):
            return self
        elif(self.enclosing != None):
            return self.enclosing.find(name)
        else:
            return False

# One state to manage the storing of variables, objects (when I get there), and functions
class State:
    def __init__(self):
        self.environment = Environment()

    def enclose(self):
        self.environment = Environment(self.environment)

    def close(self):
        enclosing = self.environment.enclosing
        for i in self.environment.variables:
            if(i in enclosing.variables):
                enclosing.setEnv(i, self.environment.getEnv(i))
        self.environment = self.environment.enclosing

state = State()