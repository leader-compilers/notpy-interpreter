from typing import List
from dataclasses import dataclass
from fractions import Fraction
from typing import Union, Optional, NewType
import pytest


@dataclass
class NumType:
    pass


@dataclass
class BoolType:
    pass


@dataclass
class StringType:
    pass


@dataclass
class NoneType:
    pass


@dataclass
class Null():
    pass


# Literals


@dataclass
class numeric_literal:
    value: Fraction
    type: NumType = NumType()

    def __init__(self, numerator, denominator=1):
        self.value = Fraction(numerator, denominator)


@dataclass
class bool_literal:
    value: bool
    type: BoolType = BoolType()


@dataclass
class string_literal:
    value: str
    type: StringType = StringType()


# Binary Operations(Arithmetic and Boolean)
@dataclass
class binary_operation:
    operator: str
    left: "AST"
    right: "AST"
    type: Optional[Union[NumType, BoolType]] = None


@dataclass
class unary_operation:
    operator: str
    operand: "AST"
    type: Optional[Union[NumType, BoolType]] = None

# String operation (Can take variable number of strings depending on the operation)


@dataclass
class string_concat:
    operator: str
    operands: List["AST"]
    type: StringType = StringType()


@dataclass
class string_slice:
    opeartor: str
    string: "AST"
    start: "AST"
    stop: "AST"
    hop: "AST" = numeric_literal(1)
    type: StringType = StringType()


# Let Expressions
@dataclass
class let_var:
    name: str
    type: Optional[Union[NumType, BoolType, StringType, NoneType]] = None

# variables


@dataclass
class let:
    variable: let_var
    e1: "AST"
    e2: "AST"
    type: Optional[Union[NumType, BoolType, StringType, NoneType]] = None

# left to typecheck


@dataclass
class identifier:
    name: str
    type: Optional[Union[NumType, BoolType, StringType, NoneType]] = None


@dataclass
class declare:
    variable: identifier
    value: "AST"
    type: Optional[Union[NumType, BoolType, StringType, NoneType]] = None


@dataclass
class get:
    variable: identifier
    type: Optional[Union[NumType, BoolType, StringType, NoneType]] = None


@dataclass
class set:
    variable: identifier
    value: "AST"
    type: Optional[Union[NumType, BoolType, StringType, NoneType]] = None

# If Expressions


@dataclass
class if_statement:
    condition: "AST"
    if_exp: "AST"
    else_exp: "AST"
    type: Optional[Union[NumType, BoolType, StringType, NoneType]] = None

# While Loops


@dataclass
class while_loop:
    condition: "AST"
    body: "AST"
    type: Optional[Union[NumType, BoolType, StringType, NoneType]] = None

# For loop


@dataclass
class for_loop:
    iterator: identifier
    initial_value: "AST"
    condition: "AST"
    updation: "AST"
    body: "AST"
    type: Optional[Union[NumType, BoolType, StringType, NoneType]] = None


@dataclass
class block:
    exps: List["AST"]
    type: Optional[Union[NumType, BoolType, StringType, NoneType]] = None


@dataclass
class print_statement:
    exps: List["AST"]
    type: NoneType = NoneType()


@dataclass
class Lists:
    value: List["AST"]


@dataclass
class cons:
    value: "AST"
    list: "AST"


@dataclass
class is_empty:
    list: "AST" = Lists([])


@dataclass
class head:
    list: "AST" = Lists([])


@dataclass
class tail:
    list: "AST" = Lists([])


# Functions
@dataclass
class Function:
    name: identifier
    parameters: List[identifier]
    body: 'AST'
    return_exp: 'AST'
    type: Optional[Union[NumType, BoolType, StringType, NoneType]] = None


@dataclass
class FunctionCall:
    function: identifier
    arguments: List['AST']


@dataclass  # to keep track of the function name and its parameters in our environment
class FunctionObject:
    parameters: List['AST']
    body: 'AST'
    return_exp: 'AST'


AST = Lists | cons | is_empty | head | tail | print_statement | for_loop | unary_operation | numeric_literal | string_literal | string_concat | string_slice | binary_operation | let | let_var | bool_literal | if_statement | while_loop | block | identifier | get | set | declare | Function | FunctionCall | Null


TypedAST = NewType('TypedAST', AST)


class TypeError(Exception):
    pass


@dataclass
class environment:
    scopes: list[dict]

    def __init__(self):
        self.scopes = [{}]

    def start_scope(self):
        self.scopes.append({})

    def end_scope(self):
        self.scopes.pop()

    def add_to_scope(self, name, value):
        if name in self.scopes[-1]:
            raise Exception(
                "Variable already defined, can't declare two variables with same name in same scope")
        self.scopes[-1][name] = value

    def get_from_scope(self, name):
        for scope in reversed(self.scopes):
            if name in scope:
                return scope[name]
        raise Exception("Variable not defined")

    def update_scope(self, name, value):
        for scope in reversed(self.scopes):
            if name in scope:
                scope[name] = value
                return
        raise Exception("Variable not defined")


def typecheck(program: AST, lexical_scope=None, type_space=None) -> TypedAST:
    if lexical_scope is None:
        lexical_scope = {}
    if type_space is None:
        type_space = environment()

    match program:
        case numeric_literal() as t:  # already typed.
            return t
        case bool_literal() as t:  # already typed.
            return t
        case string_literal() as t:  # already typed.
            return t
        case Null() as t:  # already typed.
            return t
        case identifier(name) as t:
            if t.type is None:
                t.type = NoneType()
                return t
            else:
                t.type = type_space.get_from_scope(name)
                return t
        case let(var, e1, e2):
            e1.type = typecheck(e1, lexical_scope, type_space).type
            var.type = e1.type
            e2.type = typecheck(e2, lexical_scope | {
                                var.name: e1.type}, type_space).type
            return let(var, e1, e2, e2.type)

        case declare(var, value):
            value.type = typecheck(value, lexical_scope, type_space).type
            type_space.add_to_scope(var.name, value.type)
            var.type = type_space.get_from_scope(var.name)
            return declare(var, value, value.type)

        case get(var):
            var.type = type_space.get_from_scope(var.name)
            return get(var, var.type)
        case set(var, value):
            value.type = typecheck(value, lexical_scope, type_space).type

            if type_space.get_from_scope(var.name) != value.type:
                raise TypeError()
            var.type = type_space.get_from_scope(var.name)
            return set(var, value, value.type)

        case unary_operation(op, operand) if op == "!":
            top = typecheck(operand, lexical_scope, type_space)
            if top.type != BoolType():
                raise TypeError()
            return unary_operation(op, operand, BoolType())
        case unary_operation(op, operand) if op == "-":
            top = typecheck(operand, lexical_scope, type_space)
            if top.type != NumType():
                raise TypeError()
            return unary_operation(op, operand, NumType())
        case binary_operation(op, left, right):
            tl = typecheck(left, lexical_scope, type_space)
            tr = typecheck(right, lexical_scope, type_space)

            if op in ["+", "-", "*", "/"]:
                if tl.type != NumType() or tr.type != NumType() or tl.type != tr.type:
                    raise TypeError()
                return binary_operation(op, tl, tr, NumType())
            elif op in ["==", "!=", "<", ">", "<=", ">="]:
                if tl.type != tr.type:
                    raise TypeError()
                return binary_operation(op, tl, tr, BoolType())
            elif op in ["and", "or"]:
                if tl.type != BoolType() or tr.type != BoolType() or tl.type != tr.type:
                    raise TypeError()
                return binary_operation(op, tl, tr, BoolType())
            else:
                raise TypeError()

        case if_statement(condition, if_exp, else_exp):
            tc = typecheck(condition, lexical_scope, type_space)
            if tc.type != BoolType():
                raise TypeError()
            tt = typecheck(if_exp, lexical_scope, type_space)
            tf = typecheck(else_exp, lexical_scope, type_space)
            if tt.type != tf.type:
                raise TypeError()
            return if_statement(tc, tt, tf, tt.type)

        case block(exps):
            type_space.start_scope()

            for i in exps:
                i.type = typecheck(i, None, type_space).type

            type_space.end_scope()

            return block(exps, NumType())

        case while_loop(condition, body):
            type_space.start_scope()
            tc = typecheck(condition, lexical_scope, type_space)
            if tc.type != BoolType():
                raise TypeError()
            tb = typecheck(body, lexical_scope, type_space)
            type_space.end_scope()
            return while_loop(tc, tb, NumType())

        case for_loop(iterator, initial_value, condition, updation, body):
            ti = typecheck(initial_value, lexical_scope, type_space)
            type_space.start_scope()
            iterator.type = ti.type
            type_space.add_to_scope(iterator.name, ti.type)

            tc = typecheck(condition, lexical_scope, type_space)
            if tc.type != BoolType():
                raise TypeError()

            tu = typecheck(updation, lexical_scope, type_space)
            tb = typecheck(body, lexical_scope, type_space)
            if tu.type != NumType() or tb.type != NumType():
                raise TypeError()
            type_space.end_scope()

            return for_loop(iterator, ti, tc, tu, tb, NumType())

        case string_concat(op, lst):
            for i in lst:
                if typecheck(i, lexical_scope, type_space).type != StringType():
                    raise TypeError()
            return string_concat(op, lst, StringType())
        case string_slice(op, string, start, stop, hop):
            ts = typecheck(string, lexical_scope, type_space)
            if ts.type != StringType():
                raise TypeError()
            tstart = typecheck(start, lexical_scope, type_space)
            if tstart.type != NumType():
                raise TypeError()
            tstop = typecheck(stop, lexical_scope, type_space)
            if tstop.type != NumType():
                raise TypeError()
            thop = typecheck(hop, lexical_scope, type_space)
            if thop.type != NumType():
                raise TypeError()
            return string_slice(op, ts, tstart, tstop, thop, StringType())
        case print_statement(exps):
            for i in exps:
                i.type = typecheck(i, lexical_scope, type_space).type
            return print_statement(exps, NoneType())

    raise TypeError()

# Bin op test


def test_1():
    e1 = numeric_literal(2)
    e2 = numeric_literal(3)
    t1 = typecheck(binary_operation("+", e1, e2))
    t2 = typecheck(binary_operation("<", e1, e2))
    assert t2.type == BoolType()
    assert t1.type == NumType()
    with pytest.raises(TypeError):
        typecheck(binary_operation("+", binary_operation("*", numeric_literal(2), numeric_literal(3)),
                  binary_operation("<", numeric_literal(2), numeric_literal(3))))

# If test


def test_2():
    e1 = numeric_literal(2)
    e2 = numeric_literal(3)
    e3 = numeric_literal(4)
    e4 = numeric_literal(5)
    t1 = typecheck(if_statement(binary_operation("<", e1, e2), e3, e4))
    assert t1.type == NumType()
    with pytest.raises(TypeError):
        typecheck(if_statement(binary_operation("+", e1, e2), e3, e4))

# String test


def test_3():
    e1 = string_literal("hello")
    e2 = string_literal("world")
    e3 = string_literal("!")
    t1 = typecheck(string_concat("concat", [e1, e2, e3]))
    assert t1.type == StringType()
    e4 = numeric_literal(1)
    e5 = numeric_literal(7)
    e6 = numeric_literal(1)
    t2 = typecheck(string_slice("slice", e1, e4, e5, e6))
    assert t2.type == StringType()

# While loop, declare, set, get, block


def test_4():
    type_space = environment()
    i = identifier("i")
    j = identifier("j")
    assert typecheck(declare(i, numeric_literal(0)),
                     None, type_space).type == NumType()
    assert typecheck(declare(j, numeric_literal(0)),
                     None, type_space).type == NumType()

    assert typecheck(set(i, numeric_literal(1)), None,
                     type_space).type == NumType()
    assert typecheck(set(j, numeric_literal(1)), None,
                     type_space).type == NumType()
    assert typecheck(get(i), None, type_space).type == NumType()
    condition = binary_operation("<", get(i), numeric_literal(10))
    assert typecheck(condition, None, type_space).type == BoolType()

    b1 = set(i, binary_operation("+", get(i), numeric_literal(1)))
    b2 = set(j, binary_operation("*", get(j), get(i)))
    body = block([b1, b2])

    assert typecheck(body, None, type_space).type == NumType()

    e = while_loop(condition, body)

    print(typecheck(e, None, type_space))

# for loop test


def test_5():
    type_space = environment()
    iterator = identifier("i")
    var = identifier("var")
    last_iterator = identifier("last_iterator")

    typecheck(declare(var, numeric_literal(0)), None, type_space)
    typecheck(declare(last_iterator, numeric_literal(0)), None, type_space)

    condition = binary_operation("<", get(iterator), numeric_literal(5))
    updation = set(iterator, binary_operation(
        "+", get(iterator), numeric_literal(1)))

    b1 = set(var, binary_operation("+", get(var), numeric_literal(1)))
    b2 = set(last_iterator, get(iterator))
    body = block([b1, b2])

    e1 = for_loop(iterator, numeric_literal(0), condition, updation, body)
    print(typecheck(e1, None, type_space))


def test_6():
    type_space = environment()  # initalising namespace
    print(typecheck(numeric_literal(0), None, type_space))
    i = identifier("x")
    print(typecheck(identifier("x"), None, type_space))
    print(typecheck(declare(identifier("x"), numeric_literal(0)), None, type_space))
    print(typecheck(identifier("x"), None, type_space))
    print(typecheck(get(identifier("x")), None, type_space))
    print(typecheck(set(identifier("x"), numeric_literal(1)), None, type_space))


# test_1()
# test_2()
# test_3()
# test_4()
# test_5()
# test_6()
