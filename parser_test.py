import unittest


from parser import parse, GraphAST
class MyTestCase(unittest.TestCase):
    def test_parser(self):
        input = "type LR 'abc def' -- def -- dfa"

        tree = parse(input)

        self.assertEqual(isinstance(tree, GraphAST), True)
        self.assertEqual(tree.type.getText() == "LR", True)
        self.assertEqual(len(tree.childs) == 1, True)

        correctText = [["abc def", "def", "dfa"]]

        for j , child in enumerate(tree.childs):
            self.assertEqual( all( c.getText() == correctText[j][i] for i, c in enumerate(child.texts)), True)


    def test_transition_in_parser(self):
        input = "type LR 'abc def' -- def -- dfa \n type transition "




if __name__ == '__main__':
    unittest.main()
