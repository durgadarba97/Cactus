from TokenType import getType
from Token import *

# this will construct the "sentence". It'll put all the lexemes together in an array list.
class Scanner:
    def __init__(self, raw, e):
        self.rawtext = raw
        self.tokens = []
        self.cursor = 0
        self.line = 1
        self.start = 0
        self.length = len(self.rawtext)
        self.error = e
        self.scan()

    # I feel like this should be recursive...
    def scan(self):
        while(self.cursor < len(self.rawtext) - 1):
            self.start = self.cursor
            char = self.getNextChar()
            isliteral = False

            # ignores whitespace
            if(char == " "):
                continue


            # Handles literal strings.
            if(char == "\""):
                # This clear the char so we can get rid of leading "
                char = ""
                
                while(self.peek() != "\""):
                    nextchar = self.getNextChar()

                    # TODO make this more like expected()
                    if(self.cursor == self.length):
                        self.line = self.line + 1
                        print("please close quotes at line :" + str(self.line))
                        exit(0)

                    if(char == "\n"):
                        line = line + 1
                    else:
                        char = char + nextchar
                self.getNextChar()
                tokentype = "string"
                isliteral = True

            else:
                # handles double lexemes.
                if(char == "!" or char == "<" or char == ">" or char == "="):
                    if(self.expected("=")):
                        nextchar = self.getNextChar()
                        char = char + nextchar              
                    # TODO This ignores the last character if it's an operator

                elif(char == "\n"):
                    self.line + self.line + 1
                tokentype = getType(char)

            if(tokentype == None):
                break

            self.tokens.append(Token(tokentype, char, isliteral, self.line))

        self.tokens.append(Token("EOF", "eof", " ", self.line))

    # Returns true if the next character is equal to the expected character c.
    def expected(self, c):
        if(self.peek() == c):
            return True
        else:
            return False
    
    # looks at next char without iterating the cursor
    def peek(self):
        return self.rawtext[self.cursor]

    # gets the next character while iterating the cursor.
    def getNextChar(self):
        self.cursor = self.cursor + 1
        return self.rawtext[self.cursor - 1]

    def toString(self):
        for i in self.tokens:
            print(i.toString())

    # helper method to deal with errors
    def throw(self, s, l):
        self.error.setError(s, l)
        self.error.throwError()

            