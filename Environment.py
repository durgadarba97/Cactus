class Environment:
    def __init__(self):  
        self.variables = {"hello": "world"}
    
    def getEnv(self, name):
        # print(self.evironment["hello"])
        return self.variables[name]
    
    def setEnv(self, name, value):
        self.variables[name] = value

# Trying a design pattern that I dont fully comprehend
class State:
    def __init__(self):
        self.environment = Environment()

    def getEnv(self, name):
        return self.environment.getEnv(name)
    
    def setEnv(self, name, value):
        self.environment.setEnv(name, value)

    def getAll(self):
        return self.environment
