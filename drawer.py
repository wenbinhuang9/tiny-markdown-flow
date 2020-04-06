
from PIL import Image, ImageDraw, ImageFont


from layout import  LRLayout, TopdownLayout
"""
1. calculate position(width, depth)for each state 
2. draw position
3. draw transition(according position)

"""
new_roman_font = ImageFont.truetype("./times-new-roman.ttf", 20)


class Box():
    def __init__(self):
        self.width = None
        self.height = None
        self.text = None
        self.shape = None

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

def startDraw(layout, draw):
    if isinstance(layout, LRLayout):
        drawLRLayout(layout, draw)
    elif isinstance(layout, TopdownLayout):
        drawTdLayout(layout, draw)

def __draw_new_right_arrow( draw, x1, y1, x2, y2):
    draw.line((x1, y1, x2, y2), fill=(0, 0, 0), width=1)


    ### draw arrow
    end_x, end_y = x2, y2
    upper_arrow_x, upperarrow_y = end_x - 5, y2 + 5
    lower_arrow_x, lower_arrow_y = end_x - 5, y2 - 5

    draw.line((upper_arrow_x, upperarrow_y, end_x, end_y), fill=(0, 0, 0), width=1)
    draw.line((lower_arrow_x, lower_arrow_y, end_x, end_y), fill=(0, 0, 0), width=1)


def draw_text(draw, x, y, str_text):
    draw.text((x, y), str_text, fill="black", font=new_roman_font)


def drawRectangle(draw, rectangle):
    point = rectangle.points()
    draw.rectangle(rectangle.points(),  fill=(230,230,250), outline=(220, 220, 250), width=1)
    text_x, text_y = rectangle.text_pos

    draw_text(draw, text_x, text_y, rectangle.text)

def createImage(width, height, file= None):
    if file == None:
        file = "lrlayout.jpg"

    im = Image.new('RGB', (width, height), (255, 255, 255))
    draw = ImageDraw.Draw(im)

    return (im,draw)

def save(im, file):
    im.save(file, format='JPEG', subsampling=0, quality=95)

def drawLRLayout(lrLayout, draw):

    for rec in lrLayout.rectangles:
        drawRectangle(draw, rec)

    for tran in lrLayout.transitions:
        x1, y1, x2, y2 = tran.x1, tran.y1, tran.x2, tran.y2
        __draw_new_right_arrow(draw, x1, y1, x2, y2 )

def drawTdLayout(topdownLayout, draw):
    for rec in topdownLayout.rectangles:
        drawRectangle(draw, rec)

    for tran in topdownLayout.transitions:
        x1, y1, x2, y2 = tran.x1, tran.y1, tran.x2, tran.y2
        __draw_new_top_down_arrow(draw, x1, y1, x2, y2 )

def __draw_new_top_down_arrow( draw, x1, y1, x2, y2):
    draw.line((x1, y1, x2, y2), fill=(0, 0, 0), width=1)

    ### draw arrow
    end_x, end_y = x2, y2
    upper_arrow_x, upperarrow_y = end_x + 5, y2 - 5
    lower_arrow_x, lower_arrow_y = end_x - 5, y2 - 5

    draw.line((upper_arrow_x, upperarrow_y, end_x, end_y), fill=(0, 0, 0), width=1)
    draw.line((lower_arrow_x, lower_arrow_y, end_x, end_y), fill=(0, 0, 0), width=1)