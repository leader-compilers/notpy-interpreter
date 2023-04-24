from bytecode import *
import lexer as l
import Parser as p
import typechecking as t
from resolver import *
from eval import *



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

    v = VM()

    e1 = []
    for i in range(4):
        e1.append(string_literal(str(i)))
    e2 = string_concat(e1)
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

    # E LENGTH
    s = identifier("s", 0)
    e1 = string_literal("Hello World")
    v.load(compile(declare(s, e1)))
    v.execute()
    i = identifier("i", 1)
    v.load(compile(declare(i, numeric_literal(1))))
    v.execute()
    v.load(compile(length(e1)))
    assert(v.execute() == 11)

    # FIND
    v.load(compile(find(e1, get(i))))
    assert(v.execute() == "e")
    v.load(compile(find(get(s), get(i),)))
    assert(v.execute() == "e")

    # PUT
    v.load(compile(put(e1, get(i), string_literal("a"))))  # i = 1
    assert(v.execute() == "Hallo World")
    # s = "Hello World"
    v.load(compile(put(get(s), get(i), string_literal("a"))))
    v.execute()
    v.load(compile(get(s)))
    assert(v.execute() == "Hallo World")


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

def test7_listOps():
    v = VM()
    # Testing empty lists
    a = identifier("a", 0)
    e1 = Lists([])
    v.load(compile(declare(a, e1)))
    v.execute()
    v.load(compile(get(a)))
    assert(v.execute() == [])

    e1 = list_initializer(numeric_literal(0), numeric_literal(0))
    v.load(compile(declare(a, e1)))
    v.execute()
    v.load(compile(get(a)))
    assert(v.execute() == [])

    # Setting an identifier as a list
    x = identifier("x", 0)
    e1 = Lists([numeric_literal(1), numeric_literal(2), numeric_literal(3)])
    v.load(compile(declare(x, e1)))
    v.execute()
    v.load(compile(get(x)))
    assert(v.execute() == [1, 2, 3])

    # Setting another identifier as a list via an identifier
    y = identifier("y", 1)
    v.load(compile(declare(y, get(x))))
    v.execute()
    v.load(compile(get(y)))
    assert(v.execute() == [1, 2, 3])

    # Setting an identifier as a list created using the initializer
    l = identifier("l", 2)
    e2 = list_initializer(numeric_literal(4), numeric_literal(1))
    v.load(compile(declare(l, e2)))
    v.execute()
    v.load(compile(get(l)))
    assert(v.execute() == [1, 1, 1, 1])

    # Tests for Head using a list directly
    e3 = u_list_operation("head", Lists(
        [numeric_literal(1), numeric_literal(2), numeric_literal(3)]))
    v.load(compile(e3))
    assert(v.execute() == 1)

    # Tests for Head using a list via an identifier
    e3 = u_list_operation("head", get(x))
    v.load(compile(e3))
    assert(v.execute() == 1)

    # Tests for Tail using a list directly
    e4 = u_list_operation("tail", Lists(
        [numeric_literal(1), numeric_literal(2), numeric_literal(3)]))
    v.load(compile(e4))
    assert(v.execute() == [2, 3])

    # Tests for Tail using a list via an identifier
    e4 = u_list_operation("tail", get(x))
    v.load(compile(e4))
    assert(v.execute() == [2, 3])

    # Tests for Is_Empty using a list directly
    e5 = u_list_operation("is_empty", Lists(
        [numeric_literal(1), numeric_literal(2), numeric_literal(3)]))
    v.load(compile(e5))
    assert(v.execute() == False)

    # Tests for Is_Empty using a list via an identifier
    e5 = u_list_operation("is_empty", get(x))
    v.load(compile(e5))
    assert(v.execute() == False)

    # The following tests also requries us to check whether the list was updated in the name_space
    # Tests for Cons using a list directly
    e6 = b_list_operation("cons", numeric_literal(0), Lists(
        [numeric_literal(1), numeric_literal(2), numeric_literal(3)]))
    v.load(compile(e6))
    assert(v.execute() == [0, 1, 2, 3])

    # Tests for Cons using a list via an identifier
    e6 = b_list_operation("cons", numeric_literal(0), get(x))
    v.load(compile(e6))
    assert(v.execute() == [0, 1, 2, 3])
    v.load(compile(get(x)))
    assert(v.execute() == [0, 1, 2, 3])

    # Tests for Append using a list directly
    e7 = b_list_operation("append", numeric_literal(4), Lists(
        [numeric_literal(1), numeric_literal(2), numeric_literal(3)]))
    v.load(compile(e7))
    assert(v.execute() == [1, 2, 3, 4])

    # Tests for Append using a list via an identifier
    e7 = b_list_operation("append", numeric_literal(4),  get(x))
    v.load(compile(e7))
    assert(v.execute() == [0, 1, 2, 3, 4])
    v.load(compile(get(x)))
    assert(v.execute() == [0, 1, 2, 3, 4])

    # Tests for lenght using a list directly
    e8 = length(
        Lists([numeric_literal(1), numeric_literal(2), numeric_literal(3)]))
    v.load(compile(e8))
    assert(v.execute() == 3)

    # Tests for lenght using a list via an identifier
    e8 = length(get(x))
    v.load(compile(e8))
    assert(v.execute() == 5)

    # Tests for Find using a list directly without and with an identifier as the index
    i1 = identifier("i1", 3)
    v.load(compile(declare(i1, numeric_literal(1))))
    v.execute()
    e9 = find(Lists([numeric_literal(1), numeric_literal(
        2), numeric_literal(3)]), numeric_literal(2))
    v.load(compile(e9))
    assert(v.execute() == 3)
    e9 = find(
        Lists([numeric_literal(1), numeric_literal(2), numeric_literal(3)]), get(i1))
    v.load(compile(e9))
    assert(v.execute() == 2)

    # Tests for Find using a list via an identifier without and with an identifier as the index
    e10 = find(get(x), numeric_literal(2))  # x = [0, 1, 2, 3, 4]
    v.load(compile(e10))
    assert(v.execute() == 2)
    e10 = find(get(x), get(i1))  # i1 = 1
    v.load(compile(e10))
    assert(v.execute() == 1)

    # The following tests also requries us to check whether the list was updated in the name_space
    # Tests for put using a list directly without and with an identifier as the index/value
    e11 = put(Lists([numeric_literal(1), numeric_literal(
        2), numeric_literal(3)]), numeric_literal(2), numeric_literal(4))
    v.load(compile(e11))
    assert(v.execute() == [1, 2, 4])
    e11 = put(Lists([numeric_literal(1), numeric_literal(2), numeric_literal(3)]), get(
        i1), binary_operation("+", get(i1), numeric_literal(10)))  # i1 = 1
    v.load(compile(e11))
    assert(v.execute() == [1, 11, 3])

    # Tests for put using a list via an identifier without and with an identifier as the index/value
    e11 = put(get(x), numeric_literal(2),
              numeric_literal(4))  # x = [0, 1, 2, 3, 4]
    v.load(compile(e11))
    v.execute() == [0, 1, 4, 3, 4]
    v.load(compile(get(x)))
    assert(v.execute() == [0, 1, 4, 3, 4])



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

def test7():
    with open("test1.txt") as f:
        code = f.read()
    code = '{' + code + '}'
    stream = l.Stream.streamFromString(code)
    tokens = l.lexer.lexerFromStream(stream)
    parse = p.Parser.call_parser(tokens)
    ast = p.Parser.parse_expr(parse)
    resolvedast = resolve(ast)
    #typedast = t.typecheck(resolvedast)

    #print(resolvedast)

    v = VM()
    v.load(compile(resolvedast))
    # print_bytecode(v.bytecode)
    v.execute()

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
# test7_listOps()
# test8_dictOps()
# test7()
