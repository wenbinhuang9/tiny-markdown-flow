

from  drawer import  drawTransitions
## manage transition
from layout import  Transition

class TransitionManager():
    def __init__(self, transitionList):
        ## rectangles, circles
        self.shapes = []
        ## what does this mean
        self.transitionList = transitionList
        self.transitionMap =   { (trans.sourceID, trans.targetID):trans for trans in self.transitionList}
        self.shapesMap = None
    def layoutList(self, layouts):
        for laylou in layouts:
            self.shapes.extend(laylou.pos)


        self.shapesMap = {shape.getID():shape for shape in self.shapes}
        return self


    def parseTransitionLayout(self):

        ans = []
        for transNode in self.transitionList:
            preShape = self.shapesMap[transNode.sourceID]
            targetShape = self.shapesMap[transNode.targetID]

            trans = preShape.getTransition(preShape, targetShape, transNode)
            ans.append(trans)

        return ans


    def drawTrans(self, draw):
        transitionList = self.parseTransitionLayout()

        drawTransitions(draw, transitionList)


