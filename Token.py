class Token:
    def __init__(self, t, lexeme, literal, linenum):
        self.type = t
        self.lexeme = lexeme
        self.literal = literal
        self.line = linenum

    def toString(self):
        return self.type + " " + self.lexeme + " " + str(self.literal)

    def isLiteral(self):
        return self.literal
    
    def getLine(self):
        return self.line