import unittest
import filecmp

from engine import interpret

class MyTestCase(unittest.TestCase):
    def test_LR(self):
        file = "test_LR1.jpg"
        interpret("type LR 'lexer analysis' -- 'parser analysis' -- layout -- draw", "test_LR1.jpg")
        correct_file = "test_LR1_correct.jpg"
        self.assertEqual(filecmp.cmp(file, correct_file), True)

    def test_Mul_LR(self):
        file = "test_LR1.jpg"
        interpret("type LR 'lexer analysis' -- 'parser analysis' -- layout -- draw \n a -- b -- c", "test_Mul_LR.jpg")
        #correct_file = "test_Mul_LR_correct.jpg"
        #self.assertEqual(filecmp.cmp(file, correct_file), True)

    def test_newLR(self):
        file = "lr.jpg"
        interpret("type LR this -- is -- left -- to -- right -- graph", file)

        correct_file = "lr_correct.jpg"
        self.assertEqual(filecmp.cmp(file, correct_file), True)

    def test_newTD(self):
        file = "td.jpg"
        correct_file = "td_correct.jpg"
        interpret("type TD this -- is -- top -- to -- down -- graph", file)

        self.assertEqual(filecmp.cmp(file, correct_file), True)

    def DefineTransition(self):
        input = "type LR  1'ancestor1 male'" \
                     " \n 2'ancestor2 male' " \
                   "\n 3'qmei female' 4'xhe male' \n 5'lming male'" \
                     "transition 1>2 2>3 3>5 "

        file ="test_DefineTransition.jpg"
        interpret(input, file)


    def test_draw_lr_circle(self):
        input = "type LR .1 -- .2 "

        file = "test_draw_lr_circle.jpg"
        interpret(input, file)

if __name__ == '__main__':
    unittest.main()
