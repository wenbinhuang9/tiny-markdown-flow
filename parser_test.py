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
        input = "type LR '1|abc def' -- 2|def -- 3|dfa \n type transition 1--2 2--3"

        tree = parse(input)

        correctAns = {("1", "2"): "", ("2", "3"):""}
        for transNode in tree.transitionNodeList:
            self.assertEqual(correctAns[transNode.sourceID, transNode.targetID] == transNode.text, True)


    def test_twolint_transition_in_parser(self):
        input = "type LR '1|abc def' -- 2|def -- 3|dfa \n 4|aff -- 5|fadf  \n type transition 1--4 2--5"

        tree = parse(input)


        correctAns = {("1", "4"): "", ("2", "5"): ""}
        for transNode in tree.transitionNodeList:
            self.assertEqual(correctAns[transNode.sourceID, transNode.targetID] == transNode.text, True)


if __name__ == '__main__':
    unittest.main()
