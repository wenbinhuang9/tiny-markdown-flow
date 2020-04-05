import unittest
import filecmp

from engine import interpret

class MyTestCase(unittest.TestCase):
    def test_LR(self):
        file = "test_LR1.jpg"
        interpret("type LR 'lexer analysis' > 'parser analysis' > layout > draw", "test_LR1.jpg")
        correct_file = "test_LR1_correct.jpg"
        self.assertEqual(filecmp.cmp(file, correct_file), True)

    def test_newLR(self):
        file = "lr.jpg"
        interpret("type LR this > is > left > to > right > graph", file)

        correct_file = "lr_correct.jpg"
        self.assertEqual(filecmp.cmp(file, correct_file), True)

    def test_newTD(self):
        file = "td.jpg"
        correct_file = "td_correct.jpg"
        interpret("type TD this > is > top > to > down > graph", file)

        self.assertEqual(filecmp.cmp(file, correct_file), True)

if __name__ == '__main__':
    unittest.main()
