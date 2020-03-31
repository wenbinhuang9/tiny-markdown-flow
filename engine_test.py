import unittest


from engine import  interpret
class MyTestCase(unittest.TestCase):
    def test_LR(self):
        interpret("type TD lexer > parser > layout > draw")


    def test_LR(self):
        interpret("type LR lexer > parser > layout > draw")

    def test_newLR(self):
        interpret("type LR this > is > left > to > right > graph", "./lr.jpg")

    def test_newTD(self):
        interpret("type TD this > is > top > to > down > graph", "./td.jpg")

if __name__ == '__main__':
    unittest.main()
