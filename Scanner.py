from TokenType import getType
from Token import *
from Error import *

# this will construct the "sentence". It'll put all the lexemes together in an array list.
# I use string comparisons, but I should use enums. This will be slow in the future. 
class Scanner:
    def __init__(self, raw):
        self.rawtext = raw
        self.tokens = []
        self.cursor = 0
        self.line = 1
        self.start = 0
        self.length = len(self.rawtext)
        self.error = Error()
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
                        self.throw("open quotation", self.line)

                    if(char == "\n"):
                        self.line = self.line + 1
                    else:
                        char = char + nextchar
                self.getNextChar()
                tokentype = "string"
                isliteral = True

            # identifies keywords and idetifiers
            elif(self.isAlpha(char)):
                while(self.isAlpha(self.peek())):
                    nextchar = self.getNextChar()
                    char = char + nextchar
                tokentype = getType(char)

                if(tokentype == None):
                    tokentype = "identifier"

            # handles literal ints and doubles. allows trailing and leading periods
            elif(self.isNum(char) or char == "."):
                while(self.isNum(self.peek()) or self.peek() == "."):
                    nextchar = self.getNextChar()
                    char = char + nextchar

                if(char.__contains__(".")):
                    tokentype = "double"
                else:
                    tokentype = "int"
                
                isliteral = True

            # handles comments
            elif(char == "\\"):
                while(self.peek() != "\\"):
                    char = self.getNextChar()

                    # TODO make this more like expected()
                    if(self.cursor == self.length):
                        self.line = self.line + 1
                        self.throw("unclosed comment", self.line)

                    if(char == "\n"):
                        self.line = self.line + 1
                self.getNextChar()
                continue
                
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
                breaks

            self.tokens.append(Token(tokentype, char, isliteral, self.line))

        self.tokens.append(Token("EOF", "eof", False, self.line))

    # Returns true if the next character is equal to the expected character c.
    def expected(self, c):
        if(self.peek() == c):
            return True
        else:
            return False
    
    # looks at next char without iterating the cursor
    # TODO proper end of line return. throws an error if the input file doesn't end with a new line
    def peek(self):
        return self.rawtext[self.cursor]

    # gets the next character while iterating the cursor.
    def getNextChar(self):
        self.cursor = self.cursor + 1
        return self.rawtext[self.cursor - 1]

    def isNum(self, value):
        if(ord(value) >= 48 and ord(value) < 58):
            return True
        else:
            return False

    def isAlpha(self, value):
        if((ord(value) >= 65 and ord(value) < 91) or (ord(value) >= 97 and ord(value) < 123)):
            return True
        else:
            return False

    def toString(self):
        for i in self.tokens:
            print(i.toString())

    # helper method to deal with errors
    def throw(self, s, l):
        self.error.setError(s, l)
        self.error.throwError()

            