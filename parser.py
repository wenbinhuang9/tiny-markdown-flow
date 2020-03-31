"""
BNF for this parser

graph->'type' text | multext
multext->text '>'multext | text
text-> ID
"""

from lexer import POINTER, TEXT, Lexer

INTERVAL_LEN = 5
class TextAST():
    def __init__(self, token):
        self.token = token

    def position(self, width, height):
        ans  = []

        ans.append((width, height, self.token))

        return ans
    def __repr__(self):
        return self.token

class MulTextAST():
    def __init__(self):
        self.text = None
        self.multext = None



    def addChildList(self, text, multext):
        self.text = text
        self.multext = multext
        return self

    def position(self, width = 0, height = 0):
        ans = []
        ans1 = self.text.position(width + 1, height)
        ans2 = self.multext.position(width + 2, height)

        ans.extend(ans1)
        ans.extend(ans2)

        return ans


    def __repr__(self):
        return ",".join([child.__repr__() for child in self.childs])
class GraphAST():
    def __init__(self, type = None, child = None):
        self.type = type
        self.child = child

    def get_type(self):
        return self.type.token

    def child(self, child):
        self.child = child

    def position(self):
        return self.child.position()

    def __repr__(self):
        return self.type.__repr__() + "," + self.child.__repr__()

class TextParser():
    def __init__(self):
        pass

    def parse(self, lex):
        token = lex.nextToken()

        return TextAST(token.value)

class MulTextParser():

    def __init__(self, text):
        self.text = text

    def parse(self, lex):
        token = lex.peak()
        token1 = lex.peak(1)

        if token1 == None:
            return self.text.parse(lex)

        text1 = self.text.parse(lex)
        token1 = lex.nextToken()
        assert  token1.value == ">"

        text2 = self.parse(lex)

        return MulTextAST().addChildList(text1, text2)



class GraphParser():
    def __init__(self , multext, text):
        self.multext = multext
        self.text = text

    def get_type(self):
        return self.text.token

    def parse(self,lex):
        token = lex.nextToken()
        if token == None or token.value != "type":
            raise ValueError("invalid input")

        graph = GraphAST()
        graph.type = self.text.parse(lex)

        multext = self.multext.parse(lex)

        graph.child = multext

        return graph


def parse( input):
    lexx = Lexer()
    lexx.run(input)

    text = TextParser()
    mulTextParser = MulTextParser(text)

    graph = GraphParser(mulTextParser, text)

    while lexx.hasNext():
        tree = graph.parse(lexx)

    return tree