
from layout import  LRLayout
from drawer import drawLRLayout
from parser import parse

def interpret(input):

    tree = parse(input)

    layout = LRLayout(tree)

    drawLRLayout(layout)

if __name__ == "__main__":

    interpret("type LR lexer > parser > layout > draw")