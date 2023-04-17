from typing import List
from dataclasses import dataclass
from fractions import Fraction
from typing import Union, Optional, NewType
import pytest
from eval import *


class TypeError(Exception):
    pass


TypedAST = NewType('TypedAST', AST)


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
            operand.type = typecheck(operand, lexical_scope, type_space).type
            if operand.type != BoolType():
                raise TypeError()
            return unary_operation(op, operand, BoolType())
        case unary_operation(op, operand) if op == "-":
            operand.type = typecheck(operand, lexical_scope, type_space).type
            if operand.type != NumType():
                raise TypeError()
            return unary_operation(op, operand, NumType())
        case binary_operation(op, left, right):
            tl = typecheck(left, lexical_scope, type_space)
            tr = typecheck(right, lexical_scope, type_space)

            if op in ["+", "-", "*", "/", "%", "^", "**", ">>", "<<", "//"]:
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
                i.type = typecheck(i, lexical_scope, type_space).type

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

        case Function(identifier(name) as v, parameters, body, return_exp):
            type_space.add_to_scope(
                name, FunctionObject(parameters, body, return_exp))
            return Function(v, parameters, body, return_exp, NoneType())

        case FunctionCall(fn, args):
            function = type_space.get_from_scope(fn.name)
            for arg in args:
                arg.type = typecheck(arg, lexical_scope, type_space).type
            assert len(function.parameters) == len(args)

            type_space.start_scope()
            for i in range(len(args)):
                type_space.add_to_scope(
                    function.parameters[i].name, args[i].type)
            for j in function.body.exps:
                j.type = typecheck(j, lexical_scope, type_space).type

            function.return_exp.type = typecheck(
                function.return_exp, lexical_scope, type_space).type
            fn.type = function.return_exp.type
            type_space.end_scope()
            return FunctionCall(fn, args, function.return_exp.type)

    raise TypeError()

# Bin op test


def test_1():
    e1 = numeric_literal(2)
    e2 = numeric_literal(3)

    t1 = typecheck(binary_operation("+", e1, e2))
    t2 = typecheck(binary_operation("<", e1, e2))
    assert t1.type == NumType()
    assert t2.type == BoolType()
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
    i = identifier.make("i")
    j = identifier.make("j")
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

    assert typecheck(e, None, type_space).type == NumType()

# for loop test


def test_5():
    type_space = environment()
    iterator = identifier.make("i")
    var = identifier.make("var")
    last_iterator = identifier.make("last_iterator")

    typecheck(declare(var, numeric_literal(0)), None, type_space)
    typecheck(declare(last_iterator, numeric_literal(0)), None, type_space)

    condition = binary_operation("<", get(iterator), numeric_literal(5))
    updation = set(iterator, binary_operation(
        "+", get(iterator), numeric_literal(1)))
    b1 = set(var, binary_operation("+", get(var), numeric_literal(1)))
    b2 = set(last_iterator, get(iterator))
    body = block([b1, b2])

    e1 = for_loop(iterator, numeric_literal(0), condition, updation, body)
    assert typecheck(e1, None, type_space).type == NumType()


def test_6():
    type_space = environment()  # initalising namespace
    print(typecheck(numeric_literal(0), None, type_space))
    i = identifier("x")
    print(typecheck(identifier("x"), None, type_space))
    print(typecheck(declare(identifier("x"), numeric_literal(0)), None, type_space))
    print(typecheck(identifier("x"), None, type_space))
    print(typecheck(get(identifier("x")), None, type_space))
    print(typecheck(set(identifier("x"), numeric_literal(1)), None, type_space))


def test_7():
    type_space = environment()
    i = identifier.make("i")
    j = identifier.make("j")
    fn = identifier.make("fn")

    e = Function(fn, [i, j], block([]), binary_operation("+", get(i), get(j)))

    f = binary_operation("+", FunctionCall(fn, [numeric_literal(15), numeric_literal(2)]),
                         FunctionCall(
        fn, [numeric_literal(12), numeric_literal(3)])
    )
    b = block([e, f])
    assert typecheck(b, None, type_space).type == NumType()

# test_1()
# test_2()
# test_3()
# test_4()
# test_5()
# test_6()
# test_7()
