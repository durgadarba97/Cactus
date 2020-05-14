class Token:
    def __init__(self, t, lexeme, literal, linenum):
        self.type = t
        self.lexeme = lexeme
        self.literal = literal
        self.line = linenum

    def toString(self):
        return self.type + " " + self.lexeme + " " + self.literal
    
    def getLine(self):
        return self.line