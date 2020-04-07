"""
BNF for this parser

graph->'type' text | multext ('\n' multex)*
multext->text '-'[text|empty]'-' multext | text
text-> ID | 'ID text'
"""
## todo support ID??? for transition
## todo this graph should has a minimal unit, the unit has ID, shape type, attribute , color, background.  redesign it.

## todo how to support transition on arrow -text-
from lexer import Lexer

class Box():
    def __init__(self):
        self.ID = None
        self.width = None
        self.height = None
        self.text = None
        self.shape = None

    def addWidth(self, width):
        self.width = width
        return self


    def addHeight(self, height):
        self.height = height
        return self

    def addText(self, text):
        self.text = text
        return  self

    def addShape(self, shape):
        self.shape = shape
        return self

    def __repr__(self):
        return self.shape + self.text

class TransitionNode():
    def __init__(self, text = ""):
        self.text = text
        self.sourceID= None
        self.targetID = None




INTERVAL_LEN = 5
RECTANGLE = "#"
CIRCLE = "."
SHAPE_SET = set(["#", "."])
class TextAST():
    def __init__(self, token):
        self.token = token
        self.shape = RECTANGLE
        self.__parse_shape()

    def __parse_shape(self):
        if len(self.token) > 0:
            if self.token[0] in SHAPE_SET:
                self.shape = self.token[0]
                self.token = self.token[1:]


    def position(self, width, height):
        ans  = []

        box = Box().addWidth(width).addHeight(height).addText(self.token).addShape(self.shape)
        ans.append(box)

        return ans
    def __repr__(self):
        return self.token



class MulTextAST():
    def __init__(self):
        self.texts = []
        self.transitions = []


    def addTransition(self, trans):
        self.transitions.append(trans)
        return self

    def add(self, text):
        self.texts.append(text)
        return self

    def position(self, width = 0, height = 0):
        ans = []
        for text in self.texts:
            ans1 = text.position(width + 1, height)

            ans.extend(ans1)

        return ans


    def __repr__(self):
       # return ",".join([child.__repr__() for child in self.childs])
        return ""
class GraphAST():
    def __init__(self, type = None):
        self.type = type
        self.childs = []

    def get_type(self):
        return self.type.token

    def add (self, child):
        self.childs.append(child)

    def position(self):
        positionList = []
        for i, child in enumerate(self.childs):
            pos = child.position(height= i)
            positionList.append(pos)

        return positionList

    def __repr__(self):
        return self.type.__repr__() + "," + self.childs.__repr__()

class TextParser():
    def __init__(self):
        pass

    def parse(self, lex):
        curToken = lex.peak()
        if curToken.value == "'":
            curVauleList = []
            lex.nextToken()
            curToken = lex.nextToken()
            while curToken.value != "'":
                curVauleList.append(curToken.value)
                curToken = lex.nextToken()

            return TextAST(" ".join(curVauleList))

        else:

            token = lex.nextToken()

            return TextAST(token.value)

class MulTextParser():

    def __init__(self, text):
        self.text = text

    def parse(self, lex):
        mulText = MulTextAST()
        mulText.add(self.text.parse(lex))
        while lex.peak()!= None and lex.peak().value != "\n":
            token1 = lex.nextToken()
            assert token1.value == "-"
            token1 = lex.peak()
            if token1.value == "-":
                lex.nextToken()
                mulText.addTransition(TransitionNode())
            else:
                text = self.text.parse(lex)
                mulText.addTransition(TransitionNode(text))
            text1 = self.text.parse(lex)

            mulText.add(text1)

        return mulText


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

        graph.add(multext)
        while lex.peak() != None:
            newline = lex.nextToken()
            assert newline.value == "\n"

            multext = self.multext.parse(lex)

            graph.add(multext)
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