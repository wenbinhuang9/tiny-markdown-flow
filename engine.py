from layout import  getLayout
from drawer import  drawBox, createImage, save
from parser import parse
from transition import TransitionManager

## todo layout responsible for giving logical height and width

## todo I have benn confused by transition  and transNode, refactor right now
## todo logicWidth and logicHeight, PhicyalWidth and physical height, these two should be sperated, and physical only depends on logicl
## todo  two cycles , can adjust arrow position in circles automatically by arrow directions.
## todo adding shape object to Box, box responsibel for rerender physical position
def interpret(input, file = None):
    tree = parse(input)

    positionList , transitionList= tree.postionAndTranstion()
    layoutList = []

    ## todo optimize here
    for pos in positionList:
        graphType = tree.get_type()
        layout = getLayout(graphType, pos, transitionList)
        layoutList.append(layout)

    transitionMangeer =  TransitionManager(transitionList).layoutList(layoutList)

    ## here has a porblem, todo  how to calculate the whole frame work width and height beautifully
    maxwidth =  max([ layout.width for layout in layoutList])
    maxheight = max([ layout.height for layout in layoutList])


    im ,draw = createImage(maxwidth, maxheight, file)


    for layout in layoutList:
        drawBox(layout, draw)

    transitionMangeer.drawTrans(draw)

    save(im, file)
if __name__ == "__main__":
    interpret("type LR lexical_analysis > parser_analysis > layout_calculation > paint")