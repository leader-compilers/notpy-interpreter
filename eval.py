import typing
from dataclasses import dataclass
from fractions import Fraction



##Literals
@dataclass
class numeric_literal:
    value: Fraction
    def __init__(self, numerator, denominator=1):
        self.value = Fraction(numerator, denominator)

@dataclass
class bool_literal:
    value: bool


## Binary Operations(Arithmetic and Boolean)
@dataclass
class binary_operation:
    operator:str
    left: "AST"
    right: "AST"

## Let Expressions
@dataclass
class let_var:
    name: str


@dataclass
class let:
    variable: let_var
    e1: "AST"
    e2: "AST"

## If Expressions
@dataclass
class if_statement:
    condition: "AST"
    if_exp: "AST"
    else_exp: "AST"

AST=numeric_literal|binary_operation|let|let_var | bool_literal | if_statement

Value=Fraction|bool

def ProgramNotSupported():
    raise Exception("Program not supported, it may be in the future versions of the language")


def eval_ast(subprogram: AST, lexical_scope={})-> Value:
    match subprogram:

        ## Let Expressions
        case let_var(name):
            if name in lexical_scope:
                return lexical_scope[name]
            else:
                raise Exception("Variable not defined")
        case let(variable, e1, e2):
            temp=eval_ast(e1, lexical_scope)
            return eval_ast(e2, lexical_scope | {variable.name : temp})
        
        ## Literals
        case numeric_literal(value):
            return value
        case bool_literal(value):
            return value

        ## Arithmetic Operations
        case binary_operation("+", left, right):
            return Fraction(eval_ast(left,lexical_scope) + eval_ast(right,lexical_scope))
        case binary_operation("-", left, right):
            return Fraction(eval_ast(left, lexical_scope) - eval_ast(right, lexical_scope))
        case binary_operation("*", left, right):
            return Fraction(eval_ast(left, lexical_scope) * eval_ast(right, lexical_scope))
        case binary_operation("/", left, right):
            if eval_ast(right) == 0:
                raise Exception("Division by zero")
            return Fraction(eval_ast(left, lexical_scope) / eval_ast(right, lexical_scope))
        case binary_operation("**", left, right):
            return Fraction(eval_ast(left, lexical_scope) ** eval_ast(right, lexical_scope))
        
        ## Boolean Operations
        case binary_operation("==", left, right):
            return bool(eval_ast(left, lexical_scope) == eval_ast(right, lexical_scope))
        case binary_operation("!=", left, right):
            return bool(eval_ast(left, lexical_scope) != eval_ast(right, lexical_scope))
        case binary_operation("<", left, right):
            return bool(eval_ast(left, lexical_scope) < eval_ast(right, lexical_scope))
        case binary_operation(">", left, right):
            return bool(eval_ast(left, lexical_scope) > eval_ast(right, lexical_scope))
        case binary_operation("&&", left, right):
            return bool(eval_ast(left, lexical_scope) and eval_ast(right, lexical_scope))
        case binary_operation("||", left, right):
            return bool(eval_ast(left, lexical_scope) or eval_ast(right, lexical_scope))

        ## If Statements
        case if_statement(condition, if_exp, else_exp):
            if eval_ast(condition, lexical_scope):
                return eval_ast(if_exp, lexical_scope)
            else:
                return eval_ast(else_exp, lexical_scope)

        
        
        

    ProgramNotSupported()
    return Fraction(0)

## Tests

# basic arithmetic
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


# let expressions
def test3():
    x=let_var("x")
    y=let_var("y")
    e=let(x, numeric_literal(4), let(y, binary_operation("+", x, numeric_literal(5)), binary_operation("*", x, y)))
    assert eval_ast(e) == Fraction(36)


# if statements
def test4():
    e1=numeric_literal(4)
    e2=numeric_literal(5)
    condition=binary_operation("<", e1, e2)
    if_exp=numeric_literal(40)
    else_exp=numeric_literal(50)
    e=if_statement(condition, if_exp, else_exp)
    assert eval_ast(e) == 40


test1()
test2()
test3()
test4()