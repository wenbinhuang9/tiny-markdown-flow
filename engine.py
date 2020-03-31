
from layout import  LRLayout, getLayout
from drawer import drawLRLayout, draw
from parser import parse

def interpret(input, file = None):

    tree = parse(input)

    layout = getLayout(tree)

    draw(layout, file)

if __name__ == "__main__":
    interpret("type LR lexical_analysis > parser_analysis > layout_calculation > paint")