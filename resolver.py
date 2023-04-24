import pprint
from typing import List
from dataclasses import dataclass
from fractions import Fraction
from eval import *


# resolver

def resolve(subprogram: AST, lexical_scope=None, name_space=None) -> AST:

    if name_space is None:
        name_space = environment()
    if lexical_scope is None:
        lexical_scope = {}

    def resolve_(subprogram: AST) -> AST:

        return resolve(subprogram, lexical_scope, name_space)

    match subprogram:
        case Null():
            return Null()
        case numeric_literal(value):
            return numeric_literal(value)
        case string_literal(value):
            return string_literal(value)
        case bool_literal(value):
            return bool_literal(value)
        case dict_literal(value):
            return dict_literal(value)
        case identifier(name):
            return name_space.get_from_scope(name)
        case let_var(name):
            if name in lexical_scope:
                return lexical_scope[name]
            else:
                raise Exception("Variable not defined")
        case let(let_var(name) as v, e1, e2):
            re1 = resolve_(e1)
            lexical_scope = lexical_scope | {name: v}
            re2 = resolve_(e2)
            return let(v, re1, re2)
        case declare(identifier(name) as v, e):
            re = resolve_(e)
            name_space.add_to_scope(name, v)
            return declare(v, re)
        case get(identifier(name)):

            return get(name_space.get_from_scope(name))
        case set(identifier(name), e):
            re = resolve_(e)
            return set(name_space.get_from_scope(name), re)
        case unary_operation(op, e):
            re = resolve_(e)
            return unary_operation(op, re)
        case binary_operation(op, e1, e2):
            re1 = resolve_(e1)
            re2 = resolve_(e2)
            return binary_operation(op, re1, re2)
        case string_concat(lst):
            return string_concat([resolve_(e) for e in lst])
        case block(exps):

            name_space.start_scope()
            r = block([resolve_(e) for e in exps])
            name_space.end_scope()
            return r
        case string_slice(string, start, stop, hop):
            rstring = resolve_(string)
            rstart = resolve_(start)
            rstop = resolve_(stop)
            rhop = resolve_(hop)
            return string_slice(rstring, rstart, rstop, rhop)
        case if_statement(condition, if_exp, else_exp):
            rcondition = resolve_(condition)
            rif_exp = resolve_(if_exp)
            relse_exp = resolve_(else_exp)
            return if_statement(rcondition, rif_exp, relse_exp)
        case while_loop(condition, body):
            rcondition = resolve_(condition)
            rbody = resolve_(body)
            return while_loop(rcondition, rbody)
        case for_loop(iterator, initial_value, condition, updation, body):
            name_space.start_scope()
            name_space.add_to_scope(iterator.name, iterator)
            ri = resolve_(iterator)
            rinitial_value = resolve_(initial_value)
            rcondition = resolve_(condition)
            rupdation = resolve_(updation)
            rbody = resolve_(body)
            name_space.end_scope()
            return for_loop(ri, rinitial_value, rcondition, rupdation, rbody)
        case print_statement(lst):
            return print_statement([resolve_(e) for e in lst])
        case Function(identifier(name) as v, parameters, body, return_exp):
            name_space.add_to_scope(name, v)
            name_space.start_scope()
            for p in parameters:
                name_space.add_to_scope(p.name, p)
            rbody = block([resolve_(e) for e in body.exps])
            rreturn_exp = resolve_(return_exp)
            name_space.end_scope()
            return Function(v, parameters, rbody, rreturn_exp)
        case FunctionCall(fn, args):
            rfn = resolve_(fn)
            rargs = [resolve_(e) for e in args]
            return FunctionCall(rfn, rargs)
        
        case Lists(lst):
            return Lists([resolve_(e) for e in lst])
        case u_list_operation(op, lst):
            rlst = resolve_(lst)
            return u_list_operation(op, rlst)
        case b_list_operation(op, lst1, lst2):
            rlst1 = resolve_(lst1)
            rlst2 = resolve_(lst2)
            return b_list_operation(op, rlst1, rlst2)
        case length(lst):
            rlst = resolve_(lst)
            return length(rlst)
        case find(lst, e):
            rlst = resolve_(lst)
            re = resolve_(e)
            return find(rlst, re)
        case put(e1, e2, e3):
            re1 = resolve_(e1)
            re2 = resolve_(e2)
            re3 = resolve_(e3)
            return put(re1, re2, re3)
        case list_initializer(e1, e2):
            re1 = resolve_(e1)
            re2 = resolve_(e2)
            return list_initializer(re1, re2)
        



pp = pprint.PrettyPrinter(indent=2)

# let expressions


def test1():

    e = let(let_var.make("a"), numeric_literal(0), let_var.make("a"))
    pp.pprint(e)
    re = resolve(e)
    pp.pprint(re)
    assert eval_ast(re) == 0


def test2():
    e = Function(identifier.make("fn"), [identifier.make("i"), identifier.make("j")], block([declare(identifier.make("test"), numeric_literal(0)), set(
        identifier.make("test"), binary_operation("^", get(identifier.make("i")), get(identifier.make("j"))))]), get(identifier.make("test")))

    program = binary_operation("+", FunctionCall(identifier.make("fn"), [numeric_literal(15), numeric_literal(
        2)]), FunctionCall(identifier.make("fn"), [numeric_literal(12), numeric_literal(3)]))

    bl = block([e, program])
    pp.pprint(bl)
    re = resolve(bl)
    pp.pprint(re)


# function calls
def test3():

    e2 = let(let_var.make("y"), numeric_literal(3), binary_operation(
        "+", let_var.make("y"), numeric_literal(5)))
    e1 = let(let_var.make("x"), numeric_literal(4), let(let_var.make("x"), binary_operation(
        "+", let_var.make("x"), numeric_literal(5)), binary_operation("*", let_var.make("x"), numeric_literal(3))))

    pp.pprint(e1)
    re = resolve(e1)
    pp.pprint(re)
    assert eval_ast(re) == 27

# factorial function


def test4():
    i = identifier.make("i")
    j = identifier.make("j")
    a1 = declare(i, numeric_literal(0))
    a2 = declare(j, numeric_literal(0))
    a3 = set(i, numeric_literal(1))
    a4 = set(j, numeric_literal(1))

    condition = binary_operation("<", get(i), numeric_literal(10))
    b1 = set(i, binary_operation("+", get(i), numeric_literal(1)))
    b2 = set(j, binary_operation("*", get(j), get(i)))
    body = block([b1, b2])
    e = while_loop(condition, body)
    mainbody = block([a1, a2, a3, a4, e])
    pp.pprint(mainbody)
    re = resolve(mainbody)
    pp.pprint(re)

# for loop
def test5():
    iterator = identifier.make("i")
    var = identifier.make("var")
    last_iterator = identifier.make("last_iterator")

    
    a1 = declare(var, numeric_literal(0))
    a2 = declare(last_iterator, numeric_literal(0))

    condition = binary_operation("<", get(iterator), numeric_literal(5))
    updation = set(iterator, binary_operation(
        "+", get(iterator), numeric_literal(1)))

    b1 = set(var, binary_operation("+", get(var), numeric_literal(1)))
    b2 = set(last_iterator, get(iterator))
    body = block([b1, b2])

    e1 = for_loop(iterator, numeric_literal(0), condition, updation, body)
    mainbody = block([a1, a2, e1])
    pp.pprint(mainbody)
    re = resolve(mainbody)
    pp.pprint(re)




# test1()
# test2()
# test3()
# test4()
# test5()
