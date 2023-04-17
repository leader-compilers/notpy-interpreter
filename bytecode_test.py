from bytecode import *

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

def test2_stringOps():
    ## CONCAT
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


    ## SLICING
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


def test4_IfElse():
    e1 = numeric_literal(4)
    e2 = numeric_literal(5)
    condition = binary_operation("<", e1, e2)
    if_exp = numeric_literal(40)
    else_exp = numeric_literal(50)
    e = if_statement(condition, if_exp, else_exp)
    v = VM()
    v.load(compile(e))
    assert v.execute() == 40

    e1 = numeric_literal(7)
    e2 = numeric_literal(5)
    condition = binary_operation("<", e1, e2)
    if_exp = numeric_literal(40)
    else_exp = numeric_literal(50)
    e = if_statement(condition, if_exp, else_exp)
    v.load(compile(e))
    assert v.execute() == 50

    #nested if else
    e1 = numeric_literal(1)
    e2 = numeric_literal(15)
    condition = binary_operation("<", e1, e2)
    e3 = numeric_literal(7)
    e4 = numeric_literal(5)
    condition2 = binary_operation("<", e3, e4)
    if_exp = if_statement(condition2, numeric_literal(90), numeric_literal(150))
    else_exp = numeric_literal(7)
    e = if_statement(condition, if_exp, else_exp)
    v.load(compile(e))
    assert v.execute() == 150

    e1 = numeric_literal(7)
    e2 = numeric_literal(5)
    e3 = numeric_literal(1)
    e4 = numeric_literal(15)
    e5 = binary_operation("+", e1, e3)
    e6 = binary_operation("+", e2, e4)
    condition = binary_operation("==", e5, e6)
    if_exp = numeric_literal(1)
    else_exp = numeric_literal(0)
    e = if_statement(condition, if_exp, else_exp)
    v.load(compile(e))
    assert v.execute() == 0

    e1 = numeric_literal(7)
    e2 = numeric_literal(5)
    e3 = numeric_literal(1)
    e4 = numeric_literal(15)
    e5 = binary_operation("+", e1, e3)
    e6 = binary_operation("+", e2, e4)
    condition = binary_operation("<", e5, e6)
    if_exp = numeric_literal(1)
    else_exp = numeric_literal(0)
    e = if_statement(condition, if_exp, else_exp)
    v.load(compile(e))
    assert v.execute() == 1

    e1 = bool_literal(False)
    e2 = bool_literal(True)
    condition = binary_operation("==", e1, e2)
    if_exp = bool_literal(True)
    else_exp = bool_literal(False)
    e = if_statement(condition, if_exp, else_exp)
    v.load(compile(e))
    assert v.execute() == False


def test5_while():
    e1 = numeric_literal(0)
    e2 = numeric_literal(10)
    condition = binary_operation("<", e1, e2)
    e3 = numeric_literal(1)
    e1 = binary_operation("+", e1, e3)
    body = block([e3, e1])
    e = while_loop(condition, body)
    v = VM()
    v.load(compile(e))
    assert v.execute() == 10


    # e1 = numeric_literal(0)
    # e2 = numeric_literal(10)
    # condition = binary_operation("<", e1, e2)
    # e3 = numeric_literal(1)
    # e4 = binary_operation("+", e1, e3)
    # e5 = numeric_literal(2)
    # e6 = binary_operation("+", e1, e5)
    # e7 = binary_operation("+", e4, e6)
    # e = while_loop(condition, e7)
    # v.load(compile(e))
    # assert v.execute() == 55

    # e1 = numeric_literal(0)
    # e2 = numeric_literal(10)
    # condition = binary_operation("<", e1, e2)
    # e3 = numeric_literal(1)
    # e4 = binary_operation("+", e1, e3)
    # e5 = numeric_literal(2)
    # e6 = binary_operation("+", e1, e5)
    # e7 = binary_operation("+", e4, e6)
    # e8 = numeric_literal(3)
    # e9 = binary_operation("+", e7, e8)
    # e = while_loop(condition, e9)
    # v.load(compile(e))
    # assert v.execute() == 58

# test1_binOps()
# test2_stringOps()
# test3_unaryOps()
test4_IfElse()
# test5_while()