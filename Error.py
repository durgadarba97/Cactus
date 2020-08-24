import sys
# Tried to set it up so that you only have Error object in each object.
# I dont know if this the most effecient.
class Error(Exception):
    def __init__(self, e = "", l = 0):
        self.err = e
        self.line = l

    # TODO change this to kwargs
    def setError(self, e, l):
        self.err = e
        self.line = l

    def throwError(self):
        print("ERROR\t:\t" + self.err + "\nOccured at line\t:\t" + str(self.line))
        sys.exit(1)

class UndeclaredVariableException(Error):
    def __init__(self):
        super(UndeclaredVariableException, self).__init__()

class EndOfLineException(Error):
    def __init__(self):
        super(EndOfLineException, self).__init__()

class MissingCharacterException(Error):
    def __init__(self):
        super(MissingCharacterException, self).__init__()

class ArgumentMismatchException(Error):
    def __init__(self):
        super(ArgumentMismatchException, self).__init__()


