import sys
from Scanner import *
 

class Cacti:
    def __init__(self):
        self.file = ""
        self.scanner = None
        self.text = ""
        self.error = Error()

        # checks to make sure there's at least 1 file.
        if(len(sys.argv) != 2):
            self.throw("please import 1 file", 0)

        else:
            self.scan(sys.argv[1])
    
    # Method to import and scan file
    def scan(self, name, error):
        try:
            self.file = open(name, "r")
        except:
            self.throw("unable to open file", 1)


        self.text = self.file.read()
        self.scanner = Scanner(self.text)
        self.scanner.toString()

        self.file.close()
        print("Success!")
    
    # helper method to deal with errors
    def throw(self, s, l):
        self.error.setError(s, l)
        self.error.throwError()

# Tried to set it up so that you only have Error object in each object.
# I dont know if this the most effecient.
class Error:
    def __init__(self, e = "", l = 0):
        self.err = e
        self.line = l

    def setError(self, e, l):
        self.err = e
        self.line = l

    def throwError(self):
        print("ERROR\t:\t" + self.err + "\nOccured at line\t:\t" + str(self.line))
        sys.exit(1)


if __name__ == "__main__":
    cacti = Cacti()
