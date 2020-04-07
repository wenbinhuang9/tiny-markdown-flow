import unittest

from lexer import Lexer
class MyTestCase(unittest.TestCase):
    def test_lexer(self):
        l = Lexer()
        input = "ef -- '.hijklmn' -- '#abc' \n  "

        l.run(input)


        token3 = l.nextToken()
        token4 = l.nextToken()
        token8 = l.nextToken()
        token5 = l.nextToken()
        token6 = l.nextToken()
        token7 = l.nextToken()

        self.assertEqual(token3.value == "ef", True)
        self.assertEqual(token4.value == "-", True)
        self.assertEqual(token8.value == "-", True)
        self.assertEqual(token5.value == "'", True)

        self.assertEqual(token6.value == ".hijklmn", True)
        self.assertEqual(token7.value == "'", True)

        self.assertEqual(l.nextToken().value == "-", True)
        self.assertEqual(l.nextToken().value == "-", True)
        self.assertEqual(l.nextToken().value == "'", True)
        self.assertEqual(l.nextToken().value == "#abc", True)
        self.assertEqual(l.nextToken().value == "'", True)

        self.assertEqual(l.nextToken().value == "\n", True)


if __name__ == '__main__':
    unittest.main()
