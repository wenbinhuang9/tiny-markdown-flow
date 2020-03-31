
from layout import  LRLayout, getLayout
from drawer import drawLRLayout, draw
from parser import parse

def interpret(input):

    tree = parse(input)

    layout = getLayout(tree)

    draw(layout)

if __name__ == "__main__":
    interpret("type TD lexer > parser > layout > draw")