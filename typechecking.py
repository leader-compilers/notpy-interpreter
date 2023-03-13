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
class mut_var:
    name: str
    type: Optional[Union[NumType, BoolType, StringType, NoneType]] = None


@dataclass
class declare:
    variable: mut_var
    value: "AST"
    type: Optional[Union[NumType, BoolType, StringType, NoneType]] = None


@dataclass
class get:
    variable: mut_var
    type: Optional[Union[NumType, BoolType, StringType, NoneType]] = None


@dataclass
class set:
    variable: mut_var
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
    iterator: mut_var(None)
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


AST = print_statement | for_loop | unary_operation | numeric_literal | string_literal | string_concat | string_slice | binary_operation | let | let_var | bool_literal | if_statement | while_loop | block | mut_var | get | set | declare


TypedAST = NewType('TypedAST', AST)


class TypeError(Exception):
    pass


Value = Fraction | bool | str


def ProgramNotSupported():
    raise Exception(
        "Program not supported, it may be in the future versions of the language")


# the name_space dictionary acts as a global variable
def eval_ast(subprogram: AST, lexical_scope=None, name_space=None) -> Value:
    if lexical_scope is None:
        lexical_scope = {}
    if name_space is None:
        name_space = environment()
    match subprogram:

        # Let Expressions
        case let_var(name):
            if name in lexical_scope:
                return lexical_scope[name]
            else:
                raise Exception("Variable not defined")

        case let(variable, e1, e2):
            temp = eval_ast(e1, lexical_scope, name_space)
            return eval_ast(e2, lexical_scope | {variable.name: temp}, name_space)

        case declare(variable, value):
            name_space.add_to_scope(variable.name, eval_ast(
                value, lexical_scope, name_space))
            return 0

        case mut_var(name):  # eval_ast might never get this node as we are using get, however, it is still here for completeness
            return name_space.get_from_scope(name)
            # if name in name_space:
            #     return name_space[name]
            # else:
            #     raise Exception("Variable not defined")

        case get(variable):
            return name_space.get_from_scope(variable.name)
            # if variable.name in name_space:
            #     return name_space[variable.name]
            # else:
            #     raise Exception("Variable not defined")

        case set(variable, value):
            name_space.update_scope(variable.name, eval_ast(
                value, lexical_scope, name_space))
            # temp = eval_ast(value, lexical_scope, name_space)
            # name_space[variable.name] = temp
            return Fraction(0)  # return value of set is always 0

        # Literals
        case numeric_literal(value):
            return value
        case bool_literal(value):
            return value
        case string_literal(value):
            return value

        # Arithmetic Operations
        case binary_operation("+", left, right):
            return Fraction(eval_ast(left, lexical_scope, name_space) + eval_ast(right, lexical_scope, name_space))
        case binary_operation("-", left, right):
            return Fraction(eval_ast(left, lexical_scope, name_space) - eval_ast(right, lexical_scope, name_space))
        case binary_operation("*", left, right):
            return Fraction(eval_ast(left, lexical_scope, name_space) * eval_ast(right, lexical_scope, name_space))
        case binary_operation("/", left, right):
            if eval_ast(right) == 0:
                raise Exception("Division by zero")
            return Fraction(eval_ast(left, lexical_scope, name_space) / eval_ast(right, lexical_scope, name_space))
        case binary_operation("^", left, right):
            return Fraction(eval_ast(left, lexical_scope, name_space) ** eval_ast(right, lexical_scope, name_space))

        # Boolean Operations
        case binary_operation("==", left, right):
            return bool(eval_ast(left, lexical_scope, name_space) == eval_ast(right, lexical_scope, name_space))
        case binary_operation("!=", left, right):
            return bool(eval_ast(left, lexical_scope, name_space) != eval_ast(right, lexical_scope, name_space))
        case binary_operation("<", left, right):
            return bool(eval_ast(left, lexical_scope, name_space) < eval_ast(right, lexical_scope, name_space))
        case binary_operation(">", left, right):
            return bool(eval_ast(left, lexical_scope, name_space) > eval_ast(right, lexical_scope, name_space))
        case binary_operation("&&", left, right):
            return bool(eval_ast(left, lexical_scope, name_space) and eval_ast(right, lexical_scope, name_space))
        case binary_operation("||", left, right):
            return bool(eval_ast(left, lexical_scope, name_space) or eval_ast(right, lexical_scope, name_space))

        # If Statements
        case if_statement(condition, if_exp, else_exp):
            if eval_ast(condition, lexical_scope, name_space):
                return eval_ast(if_exp, lexical_scope, name_space)
            else:
                return eval_ast(else_exp, lexical_scope, name_space)

        # While Loops
        case while_loop(condition, body):
            while eval_ast(condition, lexical_scope, name_space):
                eval_ast(body, lexical_scope, name_space)
            return Fraction(0)  # return value of while loop is always 0

        # Blocks
        # using scoping as used in c++, inside loops, for funcitons, different scoping rules to be used.
        case block(exps):
            # if value of declared variables is changed inside the block, it will be changed outside the block
            # if new variables are declared inside the block, they will not be accessible outside the block
            name_space.start_scope()
            for exp in exps:
                eval_ast(exp, lexical_scope, name_space)
            name_space.end_scope()
            return Fraction(0)  # return value of block is always 0

        case unary_operation("!", condition):
            value = eval_ast(condition, lexical_scope, name_space)
            return not value

        case unary_operation("-", condition):
            return -(eval_ast(condition, lexical_scope, name_space))

        # String operations
        case string_concat(string_list):
            # Initializing an empty string literal
            final_string = eval_ast(string_literal(
                ""), lexical_scope, name_space)
            for i in string_list:
                # Traversing through the list of stings and concatenating them
                final_string += eval_ast(i, lexical_scope, name_space)
            return str(final_string)

        case string_slice(string, start, stop, hop):
            # Evaluating the string literal
            # Converting the factions to int as python only takes int for slicing
            begin = int(eval_ast(start))
            end = int(eval_ast(stop))
            step = int(eval_ast(hop))
            final_string = eval_ast(string, lexical_scope, name_space)
            # Doing the appropriate slicing using python's inbuilt slicing method
            return str(final_string[begin:end:step])

        case for_loop(iterator, condition, updation, body):
            while eval_ast(condition, lexical_scope, name_space):
                eval_ast(body, lexical_scope, name_space)
                eval_ast(updation, lexical_scope, name_space)
            return Fraction(0)

        case print_statement(expr_list):
            return_val = ""
            for expr in expr_list:
                value = eval_ast(expr, lexical_scope, name_space)
                return_val += str(value)
                print(value, end=" ")
            print("")
            return return_val

    ProgramNotSupported()
    return Fraction(0)


def typecheck(program: AST, env=None) -> TypedAST:
    match program:
        case numeric_literal() as t:  # already typed.
            return t
        case bool_literal() as t:  # already typed.
            return t
        case string_literal() as t:  # already typed.
            return t

        case unary_operation(op, operand) if op == "!":
            top = typecheck(operand)
            if top.type != BoolType():
                raise TypeError()
            return unary_operation(op, operand, BoolType())
        case unary_operation(op, operand) if op == "-":
            top = typecheck(operand)
            if top.type != NumType():
                raise TypeError()
            return unary_operation(op, operand, NumType())
        case binary_operation(op, left, right):
            tl = typecheck(left)
            tr = typecheck(right)
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
            tc = typecheck(condition)
            if tc.type != BoolType():
                raise TypeError()
            tt = typecheck(if_exp)
            tf = typecheck(else_exp)
            if tt.type != tf.type:
                raise TypeError()
            return if_statement(tc, tt, tf, tt.type)

        case block(exps):
            for i in exps:
                typecheck(i)
            return block(exps, NumType())

        case declare(var, value):
            tv = typecheck(value)
            var.type = tv.type
            return declare(var, tv, tv.type)
        case get(var):
            if var.type == NoneType:
                raise TypeError()  # variable not declared
            return get(var, var.type)
        case set(var, value):
            tv = typecheck(value)
            if var.type != tv.type:
                raise TypeError()
            return set(var, tv, tv.type)

        case while_loop(condition, body):
            tc = typecheck(condition)
            if tc.type != BoolType():
                raise TypeError()
            tb = typecheck(body)
            return while_loop(tc, tb, NumType())

        case for_loop(iterator, condition, updation, body):

            tc = typecheck(condition)
            if tc.type != BoolType():
                raise TypeError()
            tu = typecheck(updation)
            tb = typecheck(body)
            return for_loop(iterator, tc, tu, tb, NumType())

        case string_concat(op, lst):
            for i in lst:
                if typecheck(i).type != StringType():
                    raise TypeError()
            return string_concat(op, lst, StringType())
        case string_slice(op, string, start, stop, hop):
            ts = typecheck(string)
            if ts.type != StringType():
                raise TypeError()
            tstart = typecheck(start)
            if tstart.type != NumType():
                raise TypeError()
            tstop = typecheck(stop)
            if tstop.type != NumType():
                raise TypeError()
            thop = typecheck(hop)
            if thop.type != NumType():
                raise TypeError()
            return string_slice(op, ts, tstart, tstop, thop, StringType())

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
    i = mut_var("i")
    j = mut_var("j")
    assert typecheck(declare(i, numeric_literal(0))).type == NumType()
    assert typecheck(declare(j, numeric_literal(0))).type == NumType()

    assert typecheck(set(i, numeric_literal(1))).type == NumType()
    assert typecheck(set(j, numeric_literal(1))).type == NumType()
    assert typecheck(get(i)).type == NumType()
    condition = binary_operation("<", get(i), numeric_literal(10))
    assert typecheck(condition).type == BoolType()

    b1 = set(i, binary_operation("+", get(i), numeric_literal(1)))
    b2 = set(j, binary_operation("*", get(j), get(i)))
    body = block([b1, b2])

    assert typecheck(body).type == NumType()
    e = while_loop(condition, body)

    assert typecheck(e).type == NumType()

# for loop test


def test_5():
    iterator = mut_var("i")
    var = mut_var("var")
    last_iterator = mut_var("last_iterator")

    assert typecheck(declare(iterator, numeric_literal(0))).type == NumType()
    assert typecheck(declare(var, numeric_literal(0))).type == NumType()
    assert typecheck(declare(last_iterator, numeric_literal(0))
                     ).type == NumType()

    condition = binary_operation("<", get(iterator), numeric_literal(5))
    updation = set(iterator, binary_operation(
        "+", get(iterator), numeric_literal(1)))

    assert typecheck(condition).type == BoolType()
    assert typecheck(updation).type == NumType()

    b1 = set(var, binary_operation("+", get(var), numeric_literal(1)))
    b2 = set(last_iterator, get(iterator))
    assert typecheck(b1).type == NumType()
    assert typecheck(b2).type == NumType()

    body = block([b1, b2])
    assert typecheck(body).type == NumType()

    e1 = for_loop(iterator, condition, updation, body)

    assert typecheck(e1).type == NumType()


test_1()
test_2()
test_3()
test_4()
test_5()
