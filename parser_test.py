import unittest


from parser import parse, GraphAST
class MyTestCase(unittest.TestCase):
    def test_parser(self):
        input = "type LR abc > def > dfa"

        tree = parse(input)

        self.assertEqual(isinstance(tree, GraphAST), True)
        print(tree)

    def test_parser1(self):
        input = "type LR 'abc def' > 'hello world"

        tree = parse(input)

        print(tree)

if __name__ == '__main__':
    unittest.main()
