from typing import List
from dataclasses import dataclass
from fractions import Fraction
from typing import Union, Optional, NewType
import pytest

# Literals


@dataclass
class numeric_literal:
    value: Fraction

    def __init__(self, numerator, denominator=1):
        self.value = Fraction(numerator, denominator)


@dataclass
class bool_literal:
    value: bool


@dataclass
class string_literal:
    value: str


# Binary Operations(Arithmetic and Boolean)
@dataclass
class binary_operation:
    operator: str
    left: "AST"
    right: "AST"


@dataclass
class unary_operation:
    operator: str
    operand: "AST"

# String operation (Can take variable number of strings depending on the operation)


@dataclass
class string_concat:
    operator: str
    operands: List["AST"]


@dataclass
class string_slice:
    opeartor: str
    string: "AST"
    start: "AST"
    stop: "AST"
    hop: "AST" = numeric_literal(1)


# Let Expressions
@dataclass
class let_var:
    name: str


# variables
@dataclass
class let:
    variable: let_var
    e1: "AST"
    e2: "AST"


@dataclass
class mut_var:
    name: str


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

# While Loops


@dataclass
class while_loop:
    condition: "AST"
    body: "AST"

# For loop


@dataclass
class for_loop:
    iterator: mut_var(None)
    condition: "AST"
    updation: "AST"
    body: "AST"


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
        case binary_operation(op, left, right) if op in ["+", "-", "*", "/", "%"]:
            tleft = typecheck(left)
            tright = typecheck(right)
            if tleft.type != numeric_literal() or tright.type != numeric_literal():
                raise TypeError()
            if op in ["+", "-", "*", "/"]:
                return binary_operation(op, left, right, numeric_literal())
            else:
                return binary_operation(op, left, right, numeric_literal(1))
        case binary_operation(op, left, right) if op in ["<", ">", "<=", ">="]:
            tleft = typecheck(left)
            tright = typecheck(right)
            if tleft.type != numeric_literal() or tright.type != numeric_literal():
                raise TypeError()
            return binary_operation(op, left, right, bool_literal())
        case binary_operation("=", left, right):
            tleft = typecheck(left)
            tright = typecheck(right)
            if tleft.type != tright.type:
                raise TypeError()
            return binary_operation("=", left, right, bool_literal())
        # case bool_operation(op, left, right) if op in ["and", "or"]:
        #     tleft = typecheck(left)
        #     tright = typecheck(right)
        #     if tleft.type != bool_literal() or tright.type != bool_literal():
        #         raise TypeError()
        #     return binary_operation(op, left, right, bool_literal())
        case unary_operation(op, operand) if op == "not":
            top = typecheck(operand)
            if top.type != bool_literal():
                raise TypeError()
            return unary_operation(op, operand, bool_literal())
        case string_literal() as t:  # already typed.
            return t
        case string_concat(op, operands):
            typed_operands = []
            for operand in operands:
                typed_operands.append(typecheck(operand))
            return string_concat(op, typed_operands, string_literal())
        case string_slice(op, string, start, stop, hop):
            typed_string = typecheck(string)
            typed_start = typecheck(start)
            typed_stop = typecheck(stop)
            typed_hop = typecheck(hop)
            if typed_string.type != string_literal() or typed_start.type != numeric_literal() \
                    or typed_stop.type != numeric_literal() or typed_hop.type != numeric_literal():
                raise TypeError()
            return string_slice(op, typed_string, typed_start, typed_stop, typed_hop, string_literal())
        case let(variable, e1, e2):
            t1 = typecheck(e1)
            env.add_to_scope(variable.name, t1)
            t2 = typecheck(e2)
            env.end_scope()
            return t2
        case mut_var(name):
            return mut_var(name)
        case declare(variable, value):
            typed_value = typecheck(value)
            env.add_to_scope(variable.name, typed_value)
            return typed_value
        case get(variable):
            return env.get_from_scope(variable.name)
        case set(variable, value):
            typed_value = typecheck(value)
            env.update_scope(variable.name, typed_value)
            return typed_value
        case if_statement(c, t, f):
            tc = typecheck(c)
            if tc.type != bool_literal():
                raise TypeError()
            tt = typecheck(t)
            tf = typecheck(f)
            if tt.type != tf.type:
                raise TypeError()
            return if_statement(tc, tt, tf, tt.type)

    raise TypeError()


def test_typecheck():

    te = typecheck(binary_operation(
        "+", numeric_literal(2), numeric_literal(3)))
    assert te.type == numeric_literal()
    te = typecheck(binary_operation(
        "<", numeric_literal(2), numeric_literal(3)))
    assert te.type == bool_literal()
    with pytest.raises(TypeError):
        typecheck(binary_operation("+", binary_operation("*", numeric_literal(2), numeric_literal(3)),
                  binary_operation("<", numeric_literal(2), numeric_literal(3))))
