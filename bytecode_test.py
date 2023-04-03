from bytecode import *

def test1_binOps():
    e1 = binary_operation("+", numeric_literal(1), numeric_literal(2))
    # assert(codegen(e1).insns == [I.PUSH(1), I.PUSH(2), I.ADD(), I.HALT()])
    v = VM()
    v.load(compile(e1))
    assert(v.execute() == 3)

def test2_stringOps():
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
    v = VM()
    v.load(compile(e4))
    assert(v.execute() == "ThisIsATestFor Concatenation")

def test4_print():
    e1 = numeric_literal(1)
    e2 = numeric_literal(2)
    e3 = string_literal("Hello")
    e4 = string_literal("World")
    e5 = bool_literal(True)
    e7 = binary_operation("+", e1, e2)
    e8 = string_concat([e3, e4])

    v = VM()
    v.load(compile(print_statement([e1])))
    assert(v.execute() == "1")
    v= VM()
    v.load(compile(print_statement([e3])))
    assert(v.execute() == "Hello")
    v = VM()
    v.load(compile(print_statement([e7])))
    assert(v.execute() == "3")
    v = VM()
    v.load(compile(print_statement([e8])))
    assert(v.execute() == "HelloWorld")
    v = VM()
    v.load(compile(print_statement([e5])))
    assert(v.execute() == "True")
    v = VM()
    v.load(compile(print_statement([e1, e2, e3, e4, e5, e7, e8])))
    assert(v.execute() == "1 2 Hello World True 3 HelloWorld")

test1_binOps()
test2_stringOps()
test4_print()