from bytecode import *
from eval import *
from resolver import *


def test():
    pass


def test1_binOps():
    v = VM()
    e1 = binary_operation("+", numeric_literal(1), numeric_literal(2))
    v.load(compile(e1))
    assert(v.execute() == 3)

    e1 = numeric_literal(4)
    e2 = numeric_literal(5)
    e3 = numeric_literal(10)
    e4 = numeric_literal(5)
    e5 = binary_operation("+", e2, e3)
    e6 = binary_operation("/", e5, e4)
    e7 = binary_operation("*", e1, e6)
    e9 = numeric_literal(7)
    e8 = binary_operation("/", e7, e9)
    v.load(compile(e8))
    assert(v.execute() == Fraction(12, 7))

    e1 = numeric_literal(4)
    e2 = numeric_literal(5)
    e3 = numeric_literal(10)
    e4 = numeric_literal(5)
    e5 = binary_operation("^", e2, e1)
    e6 = binary_operation("*", e3, e4)
    e7 = binary_operation("/", e5, e6)
    v.load(compile(e7))
    assert(v.execute() == Fraction(625, 50))

    e1 = numeric_literal(4)
    e2 = numeric_literal(2)
    e3 = binary_operation("//", e1, e2)
    v.load(compile(e3))
    assert(v.execute() == 2)
    e4 = binary_operation("%", e1, e2)
    v.load(compile(e4))
    assert(v.execute() == 0)

    e1 = numeric_literal(4)
    e2 = numeric_literal(2)
    e3 = binary_operation("==", e1, e2)
    v.load(compile(e3))
    assert(v.execute() == False)
    e4 = binary_operation("!=", e1, e2)
    v.load(compile(e4))
    assert(v.execute() == True)

    e5 = binary_operation(">", e1, e2)
    v.load(compile(e5))
    assert(v.execute() == True)
    e6 = binary_operation("<", e1, e2)
    v.load(compile(e6))
    assert(v.execute() == False)
    e7 = binary_operation(">=", e1, e2)
    v.load(compile(e7))
    assert(v.execute() == True)

    e8 = binary_operation("&&", e5, e6)
    v.load(compile(e8))
    assert(v.execute() == False)
    e9 = binary_operation("||", e5, e6)
    v.load(compile(e9))
    assert(v.execute() == True)

    e3 = bool_literal(True)
    e2 = bool_literal(False)
    e1 = string_literal("hello")
    e4 = binary_operation("&&", e2, e3)
    e5 = binary_operation("&&", e1, e4)
    v.load(compile(e5))
    assert(v.execute() == False)


def test2_stringOps():
    # CONCAT
    e1 = []
    for i in range(4):
        e1.append(string_literal(str(i)))
    e2 = string_concat(e1)
    v = VM()
    v.load(compile(e2))
    assert(v.execute() == "0123")

    words = ["This", "Is", "A", "Test", "For", " ", "Concatenation"]
    e3 = []
    for i in words:
        e3.append(string_literal(i))
    e4 = string_concat(e3)
    v.load(compile(e4))
    assert(v.execute() == "ThisIsATestFor Concatenation")

    # SLICING
    e1 = string_literal("HelloWorld")
    minusone = numeric_literal(-1)
    zero = numeric_literal(0)
    one = numeric_literal(1)
    two = numeric_literal(2)
    four = numeric_literal(4)
    ten = numeric_literal(10)
    e2 = string_slice(e1, zero, four, one)
    v.load(compile(e2))
    assert(v.execute() == "Hell")
    e3 = string_slice(e1, zero, ten, two)
    v.load(compile(e3))
    assert(v.execute() == "Hlool")
    e4 = string_slice(e1, four, zero, minusone)
    v = VM()
    v.load(compile(e4))
    assert(v.execute() == "olle")


def test3_unaryOps():
    e1 = numeric_literal(1)
    e2 = numeric_literal(1)
    e3 = unary_operation("!", binary_operation("==", e1, e2))
    v = VM()
    v.load(compile(e3))
    assert(v.execute() == False)

    e1 = numeric_literal(1)
    e2 = numeric_literal(0)
    e3 = unary_operation("!", binary_operation("==", e1, e2))
    v.load(compile(e3))
    assert(v.execute() == True)

    e1 = string_literal("Hello")
    e2 = string_literal("Hello")
    e3 = unary_operation("!", binary_operation("==", e1, e2))
    v.load(compile(e3))
    assert(v.execute() == False)

    e1 = numeric_literal(1)
    e2 = unary_operation("-", e1)
    v.load(compile(e2))
    assert(v.execute() == -1)

    e1 = numeric_literal(-1)
    e2 = unary_operation("-", e1)
    v.load(compile(e2))
    assert(v.execute() == 1)




def test4():
    a1 = declare(identifier("a", 0), numeric_literal(1))
    a2 = set(identifier("a", 0), binary_operation(
        "+", get(identifier("a", 0)), numeric_literal(1)))
    a3 = print_statement([get(identifier("a", 0))])
    b = block([a1, a2, a3])
    v = VM()
    v.load(compile(b))
    # print(v.insns)
    v.execute()


def test6():

    e1 = declare(identifier.make("i"), numeric_literal(0))
    e2 = declare(identifier.make("j"), numeric_literal(0))
    e3 = set(identifier.make("i"), numeric_literal(1))
    e4 = set(identifier.make("j"), numeric_literal(1))
    condition = binary_operation(
        "<", get(identifier.make("i")), numeric_literal(10))
    b1 = set(identifier.make("i"), binary_operation(
        "+", get(identifier.make("i")), numeric_literal(1)))
    b2 = set(identifier.make("j"), binary_operation(
        "*", get(identifier.make("j")), get(identifier.make("i"))))
    b3 = print_statement([get(identifier.make("i"))])
    body = block([b1, b2, b3])
    e = while_loop(condition, body)

    el = print_statement([get(identifier.make("j"))])
    program = block([e1, e2, e3, e4, e, el])
    ast = resolve(program)
    print(ast)
    v = VM()
    v.load(compile(ast))
    v.execute()

def test4_print():
    e1 = numeric_literal(1)
    e2 = numeric_literal(2)
    e3 = string_literal("Hello")
    e4 = string_literal("World")
    e5 = bool_literal(True)
    e7 = binary_operation("+", e1, e2)

    v = VM()
    v.load(compile(print_statement([e1])))
    v.execute()
    v= VM()
    v.load(compile(print_statement([e3])))
    v.execute()
    v = VM()
    v.load(compile(print_statement([e7])))
    v.execute()
    v = VM()
    v.load(compile(print_statement([e5])))
    v.execute()
    v = VM()
    v.load(compile(print_statement([e1, e2, e3, e4, e5, e7])))
    print_bytecode(compile(print_statement([e1, e2, e3, e4, e5, e7])))
    v.execute()



# test1_binOps()
# test2_stringOps()
# test3_unaryOps()
# test4()
test4_print()
# test6()