class Environment:
    def __init__(self, enclose = None):  
        self.variables = {"hello": "world"}
        self.enclosing = enclose
    
    # recursively checks if variable exists. Done like this for variable scoping
    def getEnv(self, name):
        # print(self.evironment["hello"])
        if(name in self.variables):
            return self.variables[name]
        elif(self.enclosing != None):
            return self.enclosing.getEnv(name)

        # TODO return error
    
    #  Because var initialization and redeclaration are the same, this recursively check if parent
    #  environment has the variable and set it at that level. If not, creates a new variable at child.
    #  Done like this for variable scoping.s
    def setEnv(self, name, value):
        found = self.find(name)

        if(found):
            found.variables[name] = value
        else:
            self.variables[name] = value

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