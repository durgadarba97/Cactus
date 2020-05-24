# defines the syntax. This is so that if I decide to change the syntax later, I just have to change it here.
# Defines the type for each lexeme. You can think of this as defining the vocabulary of the language. 

generaltypes = {
    "(" : "leftparenthesis",
    ")" : "rightparenthesis" ,
    "}" : "rightbrace",
    "{" : "leftbrace",

    "," : "comma",
    "\"": "quote",
    "." : "period",
    "-" : "minus",
    "+" : "plus",

    # TODO I think every line should end in a new line character. semi colons are bloated. Will change this later.
    ";" : "semicolon",
    "\\": "slash",
    "*" : "multiply",
    "=" : "equal",
    "==": "equalequal",
    "!" : "not",
    "!=": "notequal",
    ">" : "greater",
    ">=": "greaterequal",
    "<" : "less",
    "<=": "lessequal",
    "class" : "class",
    "else" : "else",
    "and" : "and",
    "or" : "or",
    "null" : "null",
    "for" : "for",
    "while" : "while",

    # TODO idk if this should be a literal. 
    "true" : "true",
    "false" : "false",

    # I'm going to change this so you can just define functions like "main()"". For now, simplicity.
    "function" : "function",
    "if" : "if",
    "print" : "print",
    "return" : "return",
    "var" : "var",
    "super" : "super",
    "\n" : "newline"
}

    # Returns the type
def getType(value):
    if(generaltypes.get(value)):
        return generaltypes[value]
    else:
        return None