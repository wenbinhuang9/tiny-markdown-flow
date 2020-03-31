import unittest


from engine import  interpret
class MyTestCase(unittest.TestCase):
    def test_LR(self):
        interpret("type TD lexer > parser > layout > draw")


    def test_LR(self):
        interpret("type LR lexer > parser > layout > draw")

if __name__ == '__main__':
    unittest.main()
