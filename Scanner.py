from TokenType import getType
from Token import *

# this will construct the "sentence". It'll put all the lexemes together in an array list.
class Scanner:
    def __init__(self, raw):
        self.rawtext = raw
        self.tokens = []
        self.cursor = 0
        self.line = 1
        self.start = 0

        self.scan()
    
    def scan(self):
        while(self.cursor < len(self.rawtext) - 1):
            self.start = self.cursor
            char = self.getNextChar()

            tokentype = getType(char)

            self.tokens.append(Token(tokentype, char, " ", self.line))
    
    def getNextChar(self):
        self.cursor = self.cursor + 1
        return self.rawtext[self.cursor]

    def toString(self):
        for i in self.tokens:
            print(i.toString())

            