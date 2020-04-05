
from layout import   getLayout
from drawer import  draw
from parser import parse

def interpret(input, file = None):

    tree = parse(input)

    positionList = tree.position()
    layoutList = []
    for pos in positionList:
        graphType = tree.get_type()
        layout = getLayout(graphType, pos)
        layoutList.append(layout)

    for layout in layoutList:
        draw(layout, file)

if __name__ == "__main__":
    interpret("type LR lexical_analysis > parser_analysis > layout_calculation > paint")