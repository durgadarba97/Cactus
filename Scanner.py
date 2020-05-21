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
        self.length = len(self.rawtext)
        self.scan()

    def scan(self):
        while(self.cursor < len(self.rawtext) - 1):
            self.start = self.cursor
            char = self.getNextChar()

            # ignores whitespace
            if(char == " "):
                continue

            # handles double lexemes.
            if(char == "!" or char == "<" or char == ">" or char == "="):
                if(self.expected("=")):
                    nextchar = self.getNextChar()
                    char = char + nextchar
                
                # TODO This ignores the last character if it's an operator

            tokentype = getType(char)

            if(tokentype == None):
                break

            self.tokens.append(Token(tokentype, char, " ", self.line))

        self.tokens.append(Token("EOF", "eof", " ", self.line))

    # Returns true if the next character is equal to the expected character c.
    def expected(self, c):
        if(self.peek() == c):
            return True
        else:
            return False
    
    # looks at next char without iterating the cursor
    def peek(self):
        # print("cursor:::" + self.rawtext[self.cursor - 1])
        # print("peek:::" + self.rawtext[self.cursor])
        return self.rawtext[self.cursor]

    # gets the next character while iterating the cursor.
    def getNextChar(self):
        self.cursor = self.cursor + 1
        return self.rawtext[self.cursor - 1]

    def toString(self):
        for i in self.tokens:
            print(i.toString())

            