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

AST=numeric_literal|binary_operation

Value=Fraction

def ProgramNotSupported():
    raise Exception("Program not supported, it may be in the future versions of the language")


def eval_ast(subprogram: AST)-> Value:
    match subprogram:
    
        case numeric_literal(value):
            return value
        case binary_operation("+", left, right):
            return eval_ast(left) + eval_ast(right)
        case binary_operation("-", left, right):
            return eval_ast(left) - eval_ast(right)
        case binary_operation("*", left, right):
            return eval_ast(left) * eval_ast(right)
        case binary_operation("/", left, right):
            if eval_ast(right) == 0:
                raise Exception("Division by zero")
            return eval_ast(left) / eval_ast(right)
        case binary_operation("**", left, right):
            return Fraction(eval_ast(left) ** eval_ast(right))

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



test1()
test2()
