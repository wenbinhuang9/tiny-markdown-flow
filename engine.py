
from layout import   getLayout
from drawer import  startDraw, createImage, save
from parser import parse

def interpret(input, file = None):

    tree = parse(input)

    positionList = tree.position()
    layoutList = []
    for pos in positionList:
        graphType = tree.get_type()
        layout = getLayout(graphType, pos)
        layoutList.append(layout)

    ## here has a porblem
    maxwidth =  max([ layout.width for layout in layoutList])
    maxheight = max([ layout.height for layout in layoutList])
    im ,draw = createImage(maxwidth, maxheight, file)

    for layout in layoutList:
        startDraw(layout, draw)

    save(im, file)
if __name__ == "__main__":
    interpret("type LR lexical_analysis > parser_analysis > layout_calculation > paint")