from parser import CIRCLE, RECTANGLE
## todo support mixture shapes
class Rectangle():
    def __init__(self, x1, y1, x2, y2, text ):
        self.left_up_x = x1
        self.left_up_y = y1
        self.bottom_right_x = x2
        self.bottom_right_y = y2
        self.text = text
        self.text_pos = None

    def points(self):
        return [self.left_up_x, self.left_up_y, self.bottom_right_x, self.bottom_right_y]

class Circle():
    def __init__(self, x1, y1, r, text = None):
        self.x1 = x1
        self.y1 = y1
        self.r = r
        self.text = text

    def points(self):
        return [self.x1, self.y1, self.r]

class Transition():
    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2



def getLayout(graphType, pos):
    if graphType == "LR":
        return LRLayout(pos)
    elif graphType == "TD":
        return TopdownLayout(pos)

    return None


class TopdownLayout():
    def __init__(self, graph):
        self.type = graph.get_type()
        self.graph = graph
        self.lrLayout = LRLayout(graph)



"""
Left to right linear layout 
"""
class LRLayout():
    def __init__(self, boxList):

        self.width = None
        self.height = None
        self.boxList = boxList

        self.width = self.boxList[-1].width
        self.height = self.boxList[-1].height

        self.x0 = 50
        self.y0 = 50
        self.padding = 10
        self.box_place = 50
        self.height = 30
        self.char_place = 8
        self.level_interval = 50
        self.pos = self.position()
        self.transitions = self.gettransition()


    def position(self):
        if self.boxList[0].shape == CIRCLE:
            return self.calCirclePosition()
        elif self.boxList[0].shape == RECTANGLE:
            return self.calPosition()

    def gettransition(self):
        if self.boxList[0].shape == CIRCLE:
            return self.circleTransition()
        elif self.boxList[0].shape == RECTANGLE:
            return self.calTransitionPos()

    def calPosition(self):
        ans = []

        accumulative_x = self.x0
        max_bottom_y = self.y0 + self.height + self.padding * 2
        for box in self.boxList:
            w,h, text, shape = box.width, box.height, box.text, box.shape
            left_top_x = accumulative_x
            accumulative_x += (len(text) * self.char_place + self.padding * 2 )
            right_bottom_x = accumulative_x
            accumulative_x += self.box_place

            left_top_y = self.x0 + self.level_interval * h + self.height * h

            right_bottom_y = left_top_y + self.height
            max_bottom_y = right_bottom_y
            rec = Rectangle(left_top_x, left_top_y, right_bottom_x, right_bottom_y, text)
            ans.append(rec)

            text_y = left_top_y + self.padding
            text_x = left_top_x + self.padding
            rec.text_pos = (text_x, text_y)

        self.width = accumulative_x  + self.box_place
        self.height = max_bottom_y + 20

        return ans


    def calCirclePosition(self):
        ans = []

        ## todo suprot
        accumulative_x = self.x0
        max_bottom_y = self.y0 + self.height + self.padding * 2
        accumulative_x = self.x0
        accumulative_y = self.y0
        for box in self.boxList:
            w,h, text, shape = box.width, box.height, box.text, box.shape

            y = self.y0 + h * self.height
            radius = max(30, len(text) * self.char_place/2 + 10)
            x = accumulative_x + self.box_place + radius
            accumulative_x = x
            ans.append(Circle(x, y, radius, text))

        self.width = accumulative_x +  100
        self.height = self.x0 + h * self.height + 50
        return ans

    def circleTransition(self):
        circleList = self.pos

        if len(circleList) == 0:
            return None
        ans = []
        pre = circleList[0]
        for i in range(1, len(circleList)):
            cur = circleList[i]
            ans.append(Transition(pre.x1 + pre.r, pre.y1, cur.x1 - cur.r, cur.y1))

        return ans

    def calTransitionPos(self):

        if len(self.pos) == 0:
            return None

        previsouRec = self.pos[0]

        ans = []
        for i in range(1, len(self.pos)):
            curRec = self.pos[i]

            x1 = previsouRec.bottom_right_x
            y1 = previsouRec.left_up_y + (previsouRec.bottom_right_y - previsouRec.left_up_y) / 2
            x2 = curRec.left_up_x
            y2 = curRec.left_up_y + (curRec.bottom_right_y - curRec.left_up_y) /2

            ans.append(Transition(x1, y1, x2, y2))
            previsouRec  = curRec
        return ans



"""
Top to down linear layout 
"""
class TopdownLayout():
    def __init__(self, boxList):

        self.width = None
        self.height = None
        self.boxList = boxList

        self.width = self.boxList[-1].width
        self.height = self.boxList[-1].height

        self.x0 = 50
        self.y0 = 50
        self.padding = 10
        self.box_place = 50
        self.height = 40
        self.char_place = 10
        self.max_len = self.getMaxTextLen()

        self.rectangles = self.calPosition()
        self.transitions = self.calTransitionPos()


    def getMaxTextLen(self):
        maxx = 0

        for box in self.boxList:
            w,h, text, shape = box.width, box.height, box.text, box.shape

            maxx =  max(maxx, len(text))

        return maxx

    def calPosition(self):
        ans = []

        left_up_x = self.x0
        right_bottom_x = self.x0 + self.max_len * self.char_place + self.padding * 2
        temp_left_up_y = self.y0
        for box in self.boxList:
            w,h, text, shape = box.width, box.height, box.text, box.shape

            left_up_y = temp_left_up_y
            right_bottom_y = left_up_y + self.height

            temp_left_up_y += self.box_place

            rec = Rectangle(left_up_x, left_up_y, right_bottom_x, right_bottom_y, text)
            ans.append(rec)

            text_y = left_up_y + self.padding
            text_x = left_up_x + self.padding
            rec.text_pos = (text_x, text_y)

        self.width = right_bottom_x + self.x0
        self.height = temp_left_up_y + self.y0

        return ans


    def calTransitionPos(self):
        if len(self.rectangles) == 0:
            return None

        previsouRec = self.rectangles[0]

        ans = []
        for i in range(1, len(self.rectangles)):
            curRec = self.rectangles[i]

            x1 = previsouRec.left_up_x + (previsouRec.bottom_right_x - previsouRec.left_up_x) /2
            y1 = previsouRec.bottom_right_y
            x2 = curRec.left_up_x + (curRec.bottom_right_x - curRec.left_up_x) /2
            y2 = curRec.left_up_y

            ans.append(Transition(x1, y1, x2, y2))
            previsouRec  = curRec
        return ans

