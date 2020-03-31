
from PIL import Image, ImageDraw


"""
1. calculate position(width, depth)for each state 
2. draw position
3. draw transition(according position)

"""


def __draw_new_right_arrow( draw, x1, y1, x2, y2):
    draw.line((x1, y1, x2, y2), fill=(0, 0, 0), width=1)


    ### draw arrow
    end_x, end_y = x2, y2
    upper_arrow_x, upperarrow_y = end_x - 10, y2 + 10
    lower_arrow_x, lower_arrow_y = end_x - 10, y2 - 10

    draw.line((upper_arrow_x, upperarrow_y, end_x, end_y), fill=(0, 0, 0), width=1)
    draw.line((lower_arrow_x, lower_arrow_y, end_x, end_y), fill=(0, 0, 0), width=1)



def draw_text(draw, x, y, str_text):
    draw.text((x, y), str_text, fill="black")


def drawRectangle(draw, rectangle):
    point = rectangle.points()
    draw.rectangle(rectangle.points(),  fill=(255, 255, 255), outline=(0, 0, 0), width=1)
    text_x, text_y = rectangle.text_pos

    draw_text(draw, text_x, text_y, rectangle.text)
def drawLRLayout(lrLayout):
    width, height = lrLayout.width, lrLayout.height

    im = Image.new('RGB', (width, height), (255, 255, 255))
    draw = ImageDraw.Draw(im)

    for rec in lrLayout.rectangles:
        drawRectangle(draw, rec)

    for tran in lrLayout.transitions:
        x1, y1, x2, y2 = tran.x1, tran.y1, tran.x2, tran.y2
        __draw_new_right_arrow(draw, x1, y1, x2, y2 )

    im.save('./new_nfa_draw.jpg', format='JPEG', subsampling=0, quality=95)


