"""
BNF for this parser

graph->'type' text | multext ('\n' multex)*
multext->text '-'[text|empty]'-' multext | text
text-> ID | 'ID text'
"""

from lexer import Lexer
from datetime import datetime
from uuid import uuid4
def uniqueID():
    eventid = datetime.now().strftime('%Y%m-%d%H-%M%S-') + str(uuid4())

    return eventid

class Box():
    def __init__(self):
        self.ID = uniqueID()
        self.width = None
        self.height = None
        self.text = None
        self.shape = None


    def addID(self, ID):
        if ID != None and ID != "":
            self.ID = ID

        return self
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

    def setSourceID(self, sourceID):
        self.sourceID =sourceID
        return self

    def setTargetID(self, targetID):
        self.targetID = targetID

        return self


INTERVAL_LEN = 5
RECTANGLE = "#"
CIRCLE = "."
SHAPE_SET = set(["#", "."])
class TextAST():
    def __init__(self, token):
        self.text = token
        self.shape = RECTANGLE
        self.ID = None

        self.__parse_ID()
        self.__parse_shape()



    def getText(self):
        return self.text

    def __parse_shape(self):
        if len(self.text) > 0:
            if self.text[0] in SHAPE_SET:
                self.shape = self.text[0]
                self.text = self.text[1:]

    def __parse_ID(self):
        if '|' in self.text:
            splitArr = self.text.split('|')
            assert len(splitArr) == 2
            self.ID = splitArr[0]
            self.text = splitArr[1]

    def position(self, width, height):
        ans  = []

        box = Box().addWidth(width).addHeight(height).addText(self.text).addShape(self.shape).addID(self.ID)
        ans.append(box)

        return ans
    def __repr__(self):
        return self.text



class MulTextAST():
    def __init__(self):
        self.texts = []
        self.transitions = []
        self.boxList = None


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

        ## this can be used in transition
        self.boxList = ans
        return ans

    def transition(self):
        ans = []
        for i in range(len(self.transitions)):
            trans = self.transitions[i]
            trans.sourceID = self.boxList[i].ID
            trans.targetID = self.boxList[i + 1].ID
            ans.append(trans)

        return ans

    def __repr__(self):
       # return ",".join([child.__repr__() for child in self.childs])
        return ""
class GraphAST():
    def __init__(self, type = None):
        self.type = type
        self.childs = []
        self.transitionNodeList = []
    def get_type(self):
        return self.type.getText()

    def add (self, child):
        self.childs.append(child)

    def addTransitionNoe(self, transitionNode):
        self.transitionNodeList.append(transitionNode)

        return self
    def postionAndTranstion(self):
        positionList = self.position()
        transitionNodeList = []

        for i , child in enumerate(self.childs):
            trans = child.transition()
            ## the children may have implicit transition
            transitionNodeList.extend(trans)

        transitionNodeList.extend(self.transitionNodeList)
        return (positionList, transitionNodeList)

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
                mulText.addTransition(TransitionNode(text.getText()))
                token1 = lex.nextToken()
                assert token1.value == "-"
            text1 = self.text.parse(lex)

            mulText.add(text1)

        return mulText

class TransitionArrowParser():

    def __init__(self, textParser):
        self.textParser = textParser


    def parse(self, lex):
        token1 = lex.nextToken()
        assert token1.value == "-"
        token1 = lex.peak()

        if token1.value == '-':
            token1 = lex.nextToken()
            assert token1.value =='-'
            return TransitionNode()
        else:
            arrowText = self.textParser.parse(lex)
            token1 = lex.nextToken()
            assert token1.value == '-'

            return TransitionNode(arrowText)


class GraphParser():
    def __init__(self , multext, text, transitonArrowParser):
        self.multext = multext
        self.text = text
        self.transitionArrowParser =  transitonArrowParser

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
        while lex.peak() != None and lex.peak().value != 'type':
            newline = lex.nextToken()
            assert newline.value == "\n"

            ## go to transition parse
            if lex.peak().value == "type":
                break
            multext = self.multext.parse(lex)

            graph.add(multext)

        if lex.peak() == None:
            return graph

        ## parse transition
        token = lex.nextToken()
        assert token.value == "type"
        token = lex.nextToken()
        assert  token.value == "transition"

        while lex.peak()!= None:
            ## this must be ID right now
            source = lex.nextToken()
            transitionNode = self.transitionArrowParser.parse(lex)

            target = lex.nextToken()

            transitionNode.setSourceID(source.getText()).setTargetID(target.getText())

            if lex.peak() == "\n":
                lex.nextToken()

            graph.addTransitionNoe(transitionNode)

        return graph


def parse( input):
    lexx = Lexer()
    lexx.run(input)

    textParser = TextParser()
    mulTextParser = MulTextParser(textParser)
    arrowParser = TransitionArrowParser(textParser)

    graph = GraphParser(mulTextParser, textParser, arrowParser)

    while lexx.hasNext():
        tree = graph.parse(lexx)

    return tree