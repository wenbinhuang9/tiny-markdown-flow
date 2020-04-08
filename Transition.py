

from  drawer import  drawTransitions
## manage transition
from layout import  Transition

class TransitionManager():
    def __init__(self):
        ## rectangles, circles
        self.shapes = None
        self.transitionMap = None


    def parseTransitionLayout(self,  f ):
        if len(self.shapes) == 0:
            return None
        pre = self.shapes[0]
        ans = []
        for i in range(1, len(self.shapes)):
            cur = self.shapes[i]
            transNode = self.transitionMap.get((pre.ID, cur.ID))
            ans.append(Transition(pre.x1 + pre.r, pre.y1, cur.x1 - cur.r, cur.y1, transNode.text))

    def draw(self):
        pass

    def circleTransition(self):
        circleList = self.pos

        if len(circleList) == 0:
            return None
        ans = []
        pre = circleList[0]
        for i in range(1, len(circleList)):
            cur = circleList[i]
            transNode = self.transitionMap.get((pre.ID, cur.ID))
            ans.append(Transition(pre.x1 + pre.r, pre.y1, cur.x1 - cur.r, cur.y1, transNode.text))

        return ans