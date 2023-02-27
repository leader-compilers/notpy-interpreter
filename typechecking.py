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
    type: Optional[Union[NumType, BoolType, StringType]] = None

# variables


@dataclass
class let:
    variable: let_var
    e1: "AST"
    e2: "AST"
    type: Optional[Union[NumType, BoolType, StringType]] = None

# left to typecheck


@dataclass
class mut_var:
    name: str
    type: Optional[Union[NumType, BoolType, StringType]] = None


@dataclass
class declare:
    variable: mut_var
    value: "AST"


@dataclass
class get:
    variable: mut_var


@dataclass
class set:
    variable: mut_var
    value: "AST"


# If Expressions
@dataclass
class if_statement:
    condition: "AST"
    if_exp: "AST"
    else_exp: "AST"
    type: Optional[Union[NumType, BoolType, StringType]] = None

# While Loops


@dataclass
class while_loop:
    condition: "AST"
    body: "AST"
    type: Optional[Union[NumType, BoolType, StringType]] = None

# For loop


@dataclass
class for_loop:
    iterator: mut_var(None)
    condition: "AST"
    updation: "AST"
    body: "AST"
    type: Optional[Union[NumType, BoolType, StringType]] = None


@dataclass
class block:
    exps: List["AST"]


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


AST = for_loop | unary_operation | numeric_literal | string_literal | string_concat | string_slice | binary_operation | let | let_var | bool_literal | if_statement | while_loop | block | mut_var | get | set | declare


TypedAST = NewType('TypedAST', AST)


class TypeError(Exception):
    pass


def typecheck(program: AST, env=None) -> TypedAST:
    match program:
        case numeric_literal() as t:  # already typed.
            return t
        case bool_literal() as t:  # already typed.
            return t
        case string_literal() as t:  # already typed.
            return t
        # case mut_var(name) as t:
        #     return t
        case unary_operation(op, operand) if op == "not":
            top = typecheck(operand)
            if top.type != BoolType():
                raise TypeError()
            return unary_operation(op, operand, BoolType())
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

        case while_loop(condition, body):
            tc = typecheck(condition)
            if tc.type != BoolType():
                raise TypeError()
            tb = typecheck(body)
            return while_loop(tc, tb, tb.type)

        case for_loop(iterator, condition, updation, body):
            tc = typecheck(condition)  # binary operation
            if tc.type != BoolType():
                raise TypeError()
            tu = typecheck(updation)  # binary operation
            if tu.type != NumType():
                raise TypeError()
            ti = typecheck(iterator)  # mut_var
            if ti.type != NumType():
                raise TypeError()
            tb = typecheck(body)
            return for_loop(ti, tc, tu, tb, tb.type)

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
        # yet to be implemented

        # case set(name, value):
        #     tv = typecheck(value)
        #     env.update_scope(name, tv)
        #     return set(name, tv, tv.type)
        # case get(name):
        #     t = env.get_from_scope(name)
        #     return get(name, t.type)
        # case declare(name, value):
        #     tv = typecheck(value)
        #     env.add_to_scope(name, tv)
        #     return declare(name, tv, tv.type)
        # case block(exps):
        #     for i in exps:
        #         typecheck(i)
        #     return block(exps, exps[-1].type)
        # case let(name, value):
        #     tv = typecheck(value)
        #     env.add_to_scope(name, tv)
        #     return let(name, tv, tv.type)
        # case let_var(name, value):
        #     tv = typecheck(value)
        #     env.add_to_scope(name, tv)
        #     return let_var(name, tv, tv.type)

    raise TypeError()


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


def test_2():
    e1 = numeric_literal(2)
    e2 = numeric_literal(3)
    e3 = numeric_literal(4)
    e4 = numeric_literal(5)
    t1 = typecheck(if_statement(binary_operation("<", e1, e2), e3, e4))
    assert t1.type == NumType()
    with pytest.raises(TypeError):
        typecheck(if_statement(binary_operation("+", e1, e2), e3, e4))


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


test_1()
test_2()
test_3()
