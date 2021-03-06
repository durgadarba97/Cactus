import sys
from Scanner import *
from Error import *
from AST import AST
 

class Cacti:
    def __init__(self):
        self.file = ""
        self.scanner = None
        self.text = ""
        self.error = Error()

        # checks to make sure there's at least 1 file.
        # if(len(sys.argv) != 2):
        #     self.throw("please import 1 file", 0)
        # else:
        #     self.scan(sys.argv[1])
        self.scan("./thorn.cactus")
        self.tokens = self.scanner.tokens

        # print("AST Construction==========>")
        self.ast = AST(self.tokens)
        
    # Method to import and scan file
    def scan(self, name):
        try:
            self.file = open(name, "r")
        except:
            self.throw("unable to open file", 1)


        self.text = self.file.read()
        self.scanner = Scanner(self.text)

        self.file.close()
        # print("Success!")
    
    # helper method to deal with errors
    def throw(self, s, l):
        self.error.setError(s, l)
        self.error.throwError()


if __name__ == "__main__":
    cacti = Cacti()
