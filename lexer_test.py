import unittest

from lexer import Lexer
class MyTestCase(unittest.TestCase):
    def test_lexer(self):
        l = Lexer()
        input = "cd > ef > 'hijklmn'"
        l.run(input)

        token1 = l.nextToken()
        token2 = l.nextToken()
        token3 = l.nextToken()
        token4 = l.nextToken()
        token5 = l.nextToken()
        token6 = l.nextToken()
        token7 = l.nextToken()

        self.assertEqual(token1.value == "cd", True)
        self.assertEqual(token2.value == ">", True)
        self.assertEqual(token3.value == "ef", True)
        self.assertEqual(token4.value == ">", True)
        self.assertEqual(token5.value == "'", True)
        self.assertEqual(token6.value == "hijklmn", True)
        self.assertEqual(token7.value == "'", True)


if __name__ == '__main__':
    unittest.main()
