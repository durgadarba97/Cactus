import sys
from Scanner import *
 

class Cacti:
    def __init__(self):
        self.file = ""
        self.hasError = False
        self.scanner = None
        self.text = ""

        # checks to make sure there's at least 1 file.
        if(len(sys.argv) != 2):
            print("Please import 1 file")
            sys.exit(1)
        else:
            self.scan(sys.argv[1])
    
    # Method to import and scan file
    def scan(self, name):
        try:
            self.file = open(name, "r")
        except:
            self.error("unable to find file", 1)

        self.text = self.file.read()
        self.scanner = Scanner(self.text)
        self.scanner.toString()

        self.file.close()
        print("Success!")
    

    # Handles throwing error
    def error(self, err, num):
        self.hasError = True
        print(err + "error code: " + str(num))
        exit(num)



if __name__ == "__main__":
    cacti = Cacti()
