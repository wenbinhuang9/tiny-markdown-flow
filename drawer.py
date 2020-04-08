
from PIL import Image, ImageDraw, ImageFont


from layout import LRLayout, TopdownLayout
"""
1. calculate position(width, depth)for each state 
2. draw position
3. draw transition(according position)

"""
new_roman_font = ImageFont.truetype("./times-new-roman.ttf", 20)




def startDraw(layout, draw):
    if isinstance(layout, LRLayout):
        drawLRLayout(layout, draw)
    elif isinstance(layout, TopdownLayout):
        drawTdLayout(layout, draw)

def __draw_new_right_arrow( draw, x1, y1, x2, y2, text = ""):
    draw_arrow(draw, x1, y1, x2, y2)
    x = int((x1 + x2) /2) - len(text)/2 * 10
    y = int((y1 + y2) / 2)
    if text != "" or text != None:
        draw_text(draw, x, y, text)

def draw_text(draw, x, y, str_text):
    if str_text == "10":
        print("here")
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

from  layout import Circle
def drawLRLayout(lrLayout, draw):

    for rec in lrLayout.pos:
        if isinstance(rec, Circle):
            __draw_cycle(draw, rec)
        else:
            drawRectangle(draw, rec)

    drawTransitions(draw, lrLayout.transitions)

def drawTransitions(draw, transitionList):
    for tran in transitionList:
        x1, y1, x2, y2, text = tran.x1, tran.y1, tran.x2, tran.y2, tran.text
        __draw_new_right_arrow(draw, x1, y1, x2, y2, text)

def drawTdLayout(topdownLayout, draw):
    for rec in topdownLayout.rectangles:
        drawRectangle(draw, rec)

    drawTransitions(draw,topdownLayout.transitions )

def __draw_new_top_down_arrow( draw, x1, y1, x2, y2):
    draw.line((x1, y1, x2, y2), fill=(0, 0, 0), width=1)

    ### draw arrow
    end_x, end_y = x2, y2
    upper_arrow_x, upperarrow_y = end_x + 5, y2 - 5
    lower_arrow_x, lower_arrow_y = end_x - 5, y2 - 5

    draw.line((upper_arrow_x, upperarrow_y, end_x, end_y), fill=(0, 0, 0), width=1)
    draw.line((lower_arrow_x, lower_arrow_y, end_x, end_y), fill=(0, 0, 0), width=1)


def __draw_cycle( draw, circle):
    x, y, r, text =  circle.x1, circle.y1, circle.r, circle.text
    leftUpPoint = (x - r, y - r)
    rightDownPoint = (x + r, y + r)
    twoPointList = [leftUpPoint, rightDownPoint]
    draw.ellipse(twoPointList, fill=(255, 255, 255), outline=(0,0,0), width=1)

    if text:
        ## todo make it in center
        draw_text(draw, x, y - 10,text )
    return draw

def __arrow( draw, end_x, end_y, dx, dy):
    cos = 0.866
    sin = 0.500
    dx, dy =  __nomalization(dx, dy)

    ### draw arrow
    upper_arrow_x, upperarrow_y = end_x + dx * cos - dy * sin, end_y + dx * sin + dy * cos

    lower_arrow_x, lower_arrow_y = end_x + dx * cos + dy * sin, end_y + dx * (-sin) + dy * cos

    draw.line((upper_arrow_x, upperarrow_y, end_x, end_y), fill=(0, 0, 0), width=1)
    draw.line((lower_arrow_x, lower_arrow_y, end_x, end_y), fill=(0, 0, 0), width=1)
def __nomalization( dx, dy):
    absolute = abs(dx) if abs(dx) > abs(dy) else abs(dy)

    if dx == 0:
        return (0, dy/(abs(dy)) * 10)

    if dy == 0:
        return (dx/abs(dx) * 10, 0)

    return (dx / (absolute + 0.0) * 10, dy / (absolute + 0.0) * 10)
def draw_arrow( draw, x1, y1, x2, y2):
    draw.line((x1, y1, x2, y2), fill=(0, 0, 0), width=1)

    dx = x1 - x2
    dy = y1 - y2
    __arrow(draw, x2, y2, dx, dy)

