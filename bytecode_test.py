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
    # print(ast)
    v = VM()
    v.load(compile(ast))
    v.execute()

def test8_dictOps():
    v = VM()
    d = identifier.make("d")
    e1 = dict_literal([(string_literal("a"), numeric_literal(1)), (string_literal("b"), numeric_literal(2))])
    e2 = declare(d, e1)
    v.load(compile(e2))
    v.execute()
    v.load(compile(get(d)))
    assert(v.execute() == {"a": 1, "b": 2})

    ## Testing u_dict_operation
    e1 = length(d)
    v.load(compile(e1))
    assert(v.execute() == 2)
    e2 = u_dict_operation("keys", d)
    v.load(compile(e2))
    assert(v.execute() == ["a", "b"])
    e3 = u_dict_operation("values", d)
    v.load(compile(e3))
    assert(v.execute() == [1, 2])
    e4 = u_dict_operation("items", d)
    v.load(compile(e4))
    assert(v.execute() == [("a", 1), ("b", 2)])


    ## Testing b_dict_operation
    e1 = find(d, string_literal("a"))
    v.load(compile(e1))
    assert(v.execute() == 1)
    e2 = find(d, string_literal("b"))
    v.load(compile(e2))
    assert(v.execute() == 2)
    e3 = b_dict_operation("delete", d, string_literal("a"))
    v.load(compile(e3))
    v.execute()
    e4 = get(d)
    v.load(compile(e4))
    assert(v.execute() == {"b": 2})
    e5 = b_dict_operation("delete", d, string_literal("b"))
    v.load(compile(e5))
    v.execute()
    e6 = get(d)
    v.load(compile(e6))
    assert(v.execute() == {})

    # ## Testing t_dict_operation
    e1 = put(d, string_literal("z"), numeric_literal(26))
    v.load(compile(e1))
    v.execute()
    e4 = get(d)
    v.load(compile(e4))
    assert(v.execute() == {"z": 26})

    e2 = put(d, string_literal("y"), numeric_literal(25))
    v.load(compile(e2))
    v.execute()
    e4 = get(d)
    v.load(compile(e4))
    assert(v.execute() == {"z": 26, "y": 25})

    e3 = put(d, string_literal("z"), numeric_literal(0))
    v.load(compile(e3))
    v.execute()
    e4 = get(d)
    v.load(compile(e4))
    assert(v.execute() == {"z": 0, "y": 25})


def test7_listOps():
    v = VM()
    x = identifier("x", 0)
    e1 = Lists([numeric_literal(1), numeric_literal(2), numeric_literal(3)])
    e2 = declare(x, e1)
    v.load(compile(e2))
    v.execute()
    v.load(compile(get(x)))
    assert(v.execute() == [1, 2, 3])


    l = identifier("l", 1)
    e3 = declare_list(l, numeric_literal(4), numeric_literal(1))
    e4 = get(l)
    v.load(compile(e3))
    v.execute()
    v.load(compile(e4))
    assert(v.execute() == [1, 1, 1, 1])


    # e3 = get(x)
    # v.load(compile(e3))
    # assert(v.execute() == [1, 2, 3])
    # assert(eval_ast(e2, None, name_space) == [1, 2, 3])

    # y = identifier.make("y")
    # eval_ast(declare(y, numeric_literal(4)), None, name_space)
    # eval_ast(set(y, e1), None, name_space)
    # assert(eval_ast(get(y), None, name_space) == [1, 2, 3])

    # ## Initlializing list ot test list operations
    # l = identifier.make("l")
    # e3 = Lists([numeric_literal(1), numeric_literal(2), numeric_literal(3)])
    # eval_ast(declare(l, e3), None, name_space)

    # ## Tests for Head
    # e4 = u_list_operation("head", l)
    # assert(eval_ast(e4, None, name_space) == 1)

    # ## Tests for Tail
    # e5 = u_list_operation("tail", l)
    # assert(eval_ast(e5, None, name_space) == [2, 3])

    # ## Tests for Is_Empty
    # e6 = u_list_operation("is_empty", l)
    # assert(eval_ast(e6, None, name_space) == False)

    # ## Tests for Cons
    # e7 = b_list_operation("cons", numeric_literal(0), l)
    # assert(eval_ast(e7, None, name_space) == [0, 1, 2, 3])


    # ## Tests for Find
    # for i in range(4):
    #     e4 = b_list_operation("find", l, numeric_literal(i))    
    #     assert(eval_ast(e4, None, name_space) == i)

    # ## Tests for Set
    # for i in range(4):
    #     e5 = t_list_operation("set", l, numeric_literal(i), numeric_literal(4))
    #     eval_ast(e5, None, name_space)
    # assert(eval_ast(get(l), None, name_space) == [4, 4, 4, 4])



# test1_binOps()
# test2_stringOps()
# test3_unaryOps()
# test4()
# test6()
test7_listOps()
test8_dictOps()
