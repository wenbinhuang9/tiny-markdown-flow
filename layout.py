from parser import CIRCLE, RECTANGLE

## todo support mixture shapes

class Rectangle():
    def __init__(self, x1, y1, x2, y2, text, box):
        self.left_up_x = x1
        self.left_up_y = y1
        self.bottom_right_x = x2
        self.bottom_right_y = y2
        self.text = text
        self.text_pos = None
        self.box = box

    def getID(self):
        return self.box.ID


    def getTransition(self, pre, cur, transNode):
        x1 = pre.bottom_right_x
        y1 = pre.left_up_y + (pre.bottom_right_y - pre.left_up_y) / 2
        x2 = cur.left_up_x
        y2 = cur.left_up_y + (cur.bottom_right_y - cur.left_up_y) / 2

        return Transition(x1, y1, x2, y2)

    def points(self):
        return [self.left_up_x, self.left_up_y, self.bottom_right_x, self.bottom_right_y]

class Circle():
    def __init__(self, x1, y1, r, text = "", ID="", box = None,):
        self.x1 = x1
        self.y1 = y1
        self.r = r
        self.text = text
        self.ID = ID
        self.box = box
    def getTransition(self, pre, cur, transNode):
        text = "" if transNode == None else transNode.getText()
        return Transition(pre.x1 + pre.r, pre.y1, cur.x1 - cur.r, cur.y1, text)
    def getID(self):
        return self.box.ID

    def points(self):
        return [self.x1, self.y1, self.r]

class Transition():
    def __init__(self, x1, y1, x2, y2, text = ""):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.text = text



def getLayout(graphType, pos, tran):
    if graphType == "LR":
        return LRLayout(pos, tran)
    elif graphType == "TD":
        return TopdownLayout(pos, tran)

    return None





"""
Left to right linear layout 
"""
class LRLayout():
    def __init__(self, boxList, transitionList):
        self.width = None
        self.height = None
        self.boxList = boxList
        self.transitionList = transitionList
        self.transitionMap = self.calTransitionMap(transitionList)
        self.width = self.boxList[-1].width
        self.height = self.boxList[-1].height
        self.height_interval   = 80
        self.x0 = 50
        self.y0 = 50
        self.padding = 10
        self.box_place = 50
        self.height = 30
        self.char_place = 8
        self.level_interval = 50
        self.pos = self.position()



    def calTransitionMap(self, transtionList):
        return { (trans.sourceID, trans.targetID):trans for trans in transtionList}

    def position(self):
        if self.boxList[0].shape == CIRCLE:
            return self.calCirclePosition()
        elif self.boxList[0].shape == RECTANGLE:
            return self.calPosition()


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
            rec = Rectangle(left_top_x, left_top_y, right_bottom_x, right_bottom_y, text, box)
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
            w,h, text, shape, ID = box.width, box.height, box.text, box.shape, box.ID

            radius = max(30, len(text) * self.char_place/2 + 10)
            y = self.y0 + h * self.height_interval

            x = accumulative_x + self.box_place + 10 + radius
            accumulative_x = x
            ans.append(Circle(x, y, radius, text, ID = ID, box = box))

        self.width = accumulative_x +  100
        self.height = self.x0 + h * self.height_interval + 50
        return ans



"""
Top to down linear layout 
"""



class TopdownLayout():
    def __init__(self, boxList, transitionList):
        self.transitionList = transitionList
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

        self.pos = self.calPosition()
        

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

            rec = Rectangle(left_up_x, left_up_y, right_bottom_x, right_bottom_y, text, box )
            ans.append(rec)

            text_y = left_up_y + self.padding
            text_x = left_up_x + self.padding
            rec.text_pos = (text_x, text_y)

        self.width = right_bottom_x + self.x0
        self.height = temp_left_up_y + self.y0

        return ans

