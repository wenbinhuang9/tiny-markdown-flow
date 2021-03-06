import re


## todo support other kinds of transition , including lexer change and parse change , adding text on transiton, good!!!
## todo refactor the code framework and  code directory
TEXT = "TEXT"
POINTER = "POINTER"
NEWLINE = "NEWLINE"
class Token():
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def getText(self):
        return self.value
    def __repr__(self):
        return "type={0},value={1}".format(self.type, self.value)
    def __str__(self):
        return "type={0},value={1}".format(self.type, self.value)

class Lexer():
    def __init__(self):
        self.tokens = []
        self.reg = "([0-9a-zA-Z_#\.\|]+|\-|\s|\')"
        self.pattern = re.compile(self.reg)
        self.pointer_sym = [">"]

    def hasNext(self):
        return  len(self.tokens) > 0

    def nextToken(self):

        token = self.tokens[0]
        self.tokens.pop(0)

        return token

    def peak(self, index = 0):
        if index >= len(self.tokens):
            return None
        return  self.tokens[index]

    def add_token(self, s):
        if s == "\n":
          self.tokens.append(Token(NEWLINE, s))
        elif s.strip() == "":
            # just empty string do nothing
            return
        elif s in self.pointer_sym:
            self.tokens.append( Token(POINTER, s))

        else:
            self.tokens.append(Token(TEXT, s))

    def run(self, input):
        begin = 0
        end = len(input)
        try:
            while begin < end:
                matched_obj = self.pattern.match(input, begin, end)
                matched_str = matched_obj.group(1)


                begin += len(matched_str)

                self.add_token(matched_str)
        except Exception as e:
            print(e)
            raise ValueError("invalid input={0}", input)
