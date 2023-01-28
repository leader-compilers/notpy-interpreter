import typing
from dataclasses import dataclass
from fractions import Fraction


@dataclass
class numeric_literal:
    value: Fraction
    def __init__(self, numerator, denominator=1):
        self.value = Fraction(numerator, denominator)

@dataclass
class binary_operation:
    operator:str
    left: "AST"
    right: "AST"


@dataclass
class let_var:
    name: str


@dataclass
class let:
    variable: let_var
    e1: "AST"
    e2: "AST"

AST=numeric_literal|binary_operation|let|let_var

Value=Fraction

def ProgramNotSupported():
    raise Exception("Program not supported, it may be in the future versions of the language")


def eval_ast(subprogram: AST, lexical_scope={})-> Value:
    match subprogram:
        case let_var(name):
            if name in lexical_scope:
                return lexical_scope[name]
            else:
                raise Exception("Variable not defined")
        case numeric_literal(value):
            return value
        case binary_operation("+", left, right):
            return eval_ast(left,lexical_scope) + eval_ast(right,lexical_scope)
        case binary_operation("-", left, right):
            return eval_ast(left, lexical_scope) - eval_ast(right, lexical_scope)
        case binary_operation("*", left, right):
            return eval_ast(left, lexical_scope) * eval_ast(right, lexical_scope)
        case binary_operation("/", left, right):
            if eval_ast(right) == 0:
                raise Exception("Division by zero")
            return eval_ast(left, lexical_scope) / eval_ast(right, lexical_scope)
        case binary_operation("**", left, right):
            return Fraction(eval_ast(left, lexical_scope) ** eval_ast(right, lexical_scope))
        case let(variable, e1, e2):
            temp=eval_ast(e1, lexical_scope)
            return eval_ast(e2, lexical_scope | {variable.name : temp})

    ProgramNotSupported()
    return Fraction(0)


def test1():
    e1 = numeric_literal(4)
    e2 = numeric_literal(5)
    e3 = numeric_literal(10)
    e4 = numeric_literal(5)
    e5 = binary_operation("+", e2, e3)
    e6 = binary_operation("/", e5, e4)
    e7 = binary_operation("*", e1, e6)
    e9= numeric_literal(7)
    e8 = binary_operation("/",e7,e9)
    assert eval_ast(e8) == Fraction(12, 7)


def test2():
    e1 = numeric_literal(4)
    e2 = numeric_literal(5)
    e3 = numeric_literal(10)
    e4 = numeric_literal(5)
    e5 = binary_operation("**", e2, e1)
    e6 = binary_operation("*", e3, e4)
    e7 = binary_operation("/", e5, e6)
    assert eval_ast(e7) == Fraction(625,50)


def test3():
    x=let_var("x")
    y=let_var("y")
    e=let(x, numeric_literal(4), let(y, binary_operation("+", x, numeric_literal(5)), binary_operation("*", x, y)))
    assert eval_ast(e) == Fraction(36)


test1()
test2()
test3()
