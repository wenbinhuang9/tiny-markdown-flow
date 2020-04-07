import unittest

from  PIL import ImageFont, ImageDraw,Image

class MyTestCase(unittest.TestCase):
    def test_font(self):
        im = Image.new('RGB', (300, 300), (255, 255, 255))
        draw = ImageDraw.Draw(im)

        # use a bitmap font
        font = ImageFont.truetype("./times-new-roman.ttf",20)

        draw.text((10, 10), "hello world", font=font, fill="black")

        im.save("./font.jpg", format='JPEG', subsampling=0, quality=95)

if __name__ == '__main__':
    unittest.main()
