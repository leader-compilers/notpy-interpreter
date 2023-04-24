from dataclasses import dataclass
from fractions import Fraction
from typing import Union, MutableMapping, List, TypeVar, Optional
from eval import *


def ProgramNotSupported():
    raise Exception(
        "Program not supported, it may be in the future versions of the language")


@dataclass
class Label:
    target: int


class I:
    """The instructions for our stack VM."""
    @dataclass
    class PUSH:
        what: Value

    @dataclass
    class UMINUS:
        pass

    @dataclass
    class ADD:
        pass

    @dataclass
    class SUB:
        pass

    @dataclass
    class MUL:
        pass

    @dataclass
    class DIV:
        pass

    @dataclass
    class QUOT:
        pass

    @dataclass
    class REM:
        pass

    @dataclass
    class EXP:
        pass

    @dataclass
    class EQ:
        pass

    @dataclass
    class NEQ:
        pass

    @dataclass
    class LT:
        pass

    @dataclass
    class GT:
        pass

    @dataclass
    class LE:
        pass

    @dataclass
    class GE:
        pass

    @dataclass
    class JMP:
        label: Label

    @dataclass
    class JMP_IF_FALSE:
        label: Label

    @dataclass
    class JMP_IF_TRUE:
        label: Label

    @dataclass
    class NOT:
        pass

    @dataclass
    class DUP:
        pass

    @dataclass
    class POP:
        pass

    @dataclass
    class LOAD:
        localID: int

    @dataclass
    class STORE:
        localID: int

    @dataclass
    class STRCAT:
        num_strings: int

    @dataclass
    class STRSLICE:
        pass

    @dataclass
    class HALT:
        pass

    @dataclass
    class PRINT:
        pass

    @dataclass
    class BUILD_LIST:
        pass

    @dataclass
    class LIST_HEAD:
        pass

    @dataclass
    class INIT_LIST:
        pass

    @dataclass
    class LIST_TAIL:
        pass

    @dataclass
    class LIST_EMPTY:
        pass

    @dataclass
    class LIST_CONS:
        pass

    @dataclass
    class LIST_APPEND:
        pass

    @dataclass
    class BUILD_DICT:
        pass

    @dataclass
    class LENGTH:
        pass

    @dataclass
    class DICT_KEYS:
        pass

    @dataclass
    class DICT_VALUES:
        pass

    @dataclass
    class DICT_ITEMS:
        pass

    @dataclass
    class FIND:
        pass

    @dataclass
    class DICT_DELETE:
        pass

    @dataclass
    class PUT:
        pass

    @dataclass
    class PUSHFN:
        entry: Label

    @dataclass
    class CALL:
        pass

    @dataclass
    class RETURN:
        pass


Instruction = (
    I.PUSH
    | I.ADD
    | I.SUB
    | I.MUL
    | I.DIV
    | I.QUOT
    | I.REM
    | I.NOT
    | I.UMINUS
    | I.JMP
    | I.JMP_IF_FALSE
    | I.JMP_IF_TRUE
    | I.DUP
    | I.POP
    | I.HALT
    | I.EQ
    | I.NEQ
    | I.LT
    | I.GT
    | I.LE
    | I.GE
    | I.LOAD
    | I.STORE
    | I.STRCAT
    | I.STRSLICE
    | I.PRINT
    | I.BUILD_LIST
    | I.LIST_HEAD
    | I.LIST_TAIL
    | I.LIST_EMPTY
    | I.LIST_CONS
    | I.LIST_APPEND
    | I.INIT_LIST
    | I.BUILD_DICT
    | I.DICT_KEYS
    | I.DICT_VALUES
    | I.DICT_ITEMS
    | I.DICT_DELETE
    | I.PUT
    | I.LENGTH
    | I.FIND
    | I.CALL
    | I.RETURN
    | I.PUSHFN
)


@dataclass
class ByteCode:
    insns: List[Instruction]

    def __init__(self):
        self.insns = []

    def label(self):
        return Label(-1)

    def emit(self, instruction):
        self.insns.append(instruction)

    def emit_label(self, label):
        label.target = len(self.insns)


@dataclass
class Frame:
    retaddr: int = -1


@dataclass
class beginFunction:
    entry: int


# class Frame:
#     locals: List[Value]

#     def __init__(self):
#         MAX_LOCALS = 32
#         self.locals = [None] * MAX_LOCALS

# global environment
global_environment: dict[int:'Value'] = {}


class VM:
    bytecode: ByteCode
    ip: int
    data: List[Value]
    currentFrame: Frame

    def load(self, bytecode):
        self.bytecode = bytecode
        self.restart()

    def restart(self):
        self.ip = 0
        self.data = []
        self.currentFrame = Frame()

    def execute(self) -> Value:
        while True:
            assert self.ip < len(self.bytecode.insns)
            match self.bytecode.insns[self.ip]:
                case I.PUSH(val):
                    self.data.append(val)
                    self.ip += 1
                case I.PUSHFN(Label(offset)):
                    self.data.append(beginFunction(offset))
                    self.ip += 1
                case I.CALL():
                    bf = self.data.pop()
                    self.currentFrame = Frame(
                        retaddr=self.ip + 1,
                    )
                    self.ip = bf.entry
                case I.RETURN():
                    self.ip = self.currentFrame.retaddr

                case I.UMINUS():
                    op = self.data.pop()
                    self.data.append(-op)
                    self.ip += 1
                case I.ADD():
                    right = self.data.pop()
                    left = self.data.pop()
                    self.data.append(left+right)
                    self.ip += 1
                case I.SUB():
                    right = self.data.pop()
                    left = self.data.pop()
                    self.data.append(left-right)
                    self.ip += 1
                case I.MUL():
                    right = self.data.pop()
                    left = self.data.pop()
                    self.data.append(left*right)
                    self.ip += 1
                case I.DIV():
                    right = self.data.pop()
                    left = self.data.pop()
                    self.data.append(left/right)
                    self.ip += 1
                case I.EXP():
                    right = self.data.pop()
                    left = self.data.pop()
                    self.data.append(left**right)
                    self.ip += 1
                case I.QUOT():
                    right = self.data.pop()
                    left = self.data.pop()
                    if left.denominator != 1 or right.denominator != 1:
                        raise ProgramNotSupported()
                    left, right = int(left), int(right)
                    self.data.append(Fraction(left // right, 1))
                    self.ip += 1
                case I.REM():
                    right = self.data.pop()
                    left = self.data.pop()
                    if left.denominator != 1 or right.denominator != 1:
                        raise ProgramNotSupported()
                    left, right = int(left), int(right)
                    self.data.append(Fraction(left % right, 1))
                    self.ip += 1
                case I.EQ():
                    right = self.data.pop()
                    left = self.data.pop()
                    self.data.append(left == right)
                    self.ip += 1
                case I.NEQ():
                    right = self.data.pop()
                    left = self.data.pop()
                    self.data.append(left != right)
                    self.ip += 1
                case I.LT():
                    right = self.data.pop()
                    left = self.data.pop()
                    self.data.append(left < right)
                    self.ip += 1
                case I.GT():
                    right = self.data.pop()
                    left = self.data.pop()
                    self.data.append(left > right)
                    self.ip += 1
                case I.LE():
                    right = self.data.pop()
                    left = self.data.pop()
                    self.data.append(left <= right)
                    self.ip += 1
                case I.GE():
                    right = self.data.pop()
                    left = self.data.pop()
                    self.data.append(left >= right)
                    self.ip += 1
                case I.JMP(label):
                    self.ip = label.target
                case I.JMP_IF_FALSE(label):
                    op = self.data.pop()
                    if not op:
                        self.ip = label.target
                    else:
                        self.ip += 1
                case I.JMP_IF_TRUE(label):
                    op = self.data.pop()
                    if op:
                        self.ip = label.target
                    else:
                        self.ip += 1
                case I.NOT():
                    op = self.data.pop()
                    self.data.append(not op)
                    self.ip += 1
                case I.DUP():
                    op = self.data.pop()
                    self.data.append(op)
                    self.data.append(op)
                    self.ip += 1
                case I.POP():
                    self.data.pop()
                    self.ip += 1
                case I.LOAD(localID):
                    # the data would be loaded from the current frame
                    # if none then error
                    # if(self.currentFrame.locals[localID] == None):
                    #     raise Exception("variable not found")
                    # self.data.append(self.currentFrame.locals[localID])
                    if localID in global_environment.keys():
                        self.data.append(global_environment[localID])
                    else:
                        raise Exception("variable not found")
                    self.ip += 1
                case I.STORE(localID):
                    v = self.data.pop()
                    global_environment[localID] = v
                    # self.currentFrame.locals[localID] = v
                    self.ip += 1
                case I.PRINT():
                    print(self.data.pop())
                    self.ip += 1
                case I.STRCAT(size):
                    string = ""
                    for i in range(size):
                        string += self.data.pop()
                    self.data.append(string)
                    self.ip += 1

                case I.STRSLICE():
                    hop = int(self.data.pop())
                    stop = int(self.data.pop())
                    start = int(self.data.pop())
                    string = self.data.pop()
                    self.data.append(string[start:stop:hop])
                    self.ip += 1

                case I.BUILD_LIST():
                    size = self.data.pop()
                    our_list = []
                    for i in range(size):
                        our_list.append(self.data.pop())
                    our_list = our_list[::-1]
                    self.data.append(our_list)
                    self.ip += 1
                case I.INIT_LIST():
                    val = self.data.pop()
                    size = int(self.data.pop())
                    our_list = []
                    for i in range(size):
                        our_list.append(val)
                    self.data.append(our_list)
                    self.ip += 1
                case I.LIST_HEAD():
                    our_list = self.data.pop()
                    if(len(our_list) == 0):
                        raise Exception("list is empty")
                    self.data.append(our_list[0])
                    self.ip += 1
                case I.LIST_TAIL():
                    our_list = self.data.pop()
                    self.data.append(our_list[1:])
                    self.ip += 1
                case I.LIST_EMPTY():
                    our_list = self.data.pop()
                    self.data.append(len(our_list) == 0)
                    self.ip += 1
                case I.LIST_CONS():
                    our_list = self.data.pop()
                    val = self.data.pop()
                    our_list.insert(0, val)
                    self.data.append(our_list)
                    self.ip += 1
                case I.LIST_APPEND():
                    our_list = self.data.pop()
                    val = self.data.pop()
                    our_list.append(val)
                    self.data.append(our_list)
                    self.ip += 1

                case I.BUILD_DICT():
                    size = self.data.pop()
                    our_dict = {}
                    for i in range(size):
                        val = self.data.pop()
                        key = self.data.pop()
                        our_dict[key] = val
                    our_dict = {k: v for k, v in reversed(our_dict.items())}
                    self.data.append(our_dict)
                    self.ip += 1
                case I.DICT_KEYS():
                    our_dict = self.data.pop()
                    self.data.append(list(our_dict.keys()))
                    self.ip += 1
                case I.DICT_VALUES():
                    our_dict = self.data.pop()
                    self.data.append(list(our_dict.values()))
                    self.ip += 1
                case I.DICT_ITEMS():
                    our_dict = self.data.pop()
                    self.data.append(list(our_dict.items()))
                    self.ip += 1
                case I.DICT_DELETE():
                    our_key = self.data.pop()
                    our_dict = self.data.pop()
                    if our_key in our_dict.keys():
                        del our_dict[our_key]
                        self.data.append(our_dict)
                    else:
                        raise Exception("key not found")
                    self.ip += 1

                case I.LENGTH():
                    data_structure = self.data.pop()
                    if isinstance(data_structure, list | dict | str):
                        self.data.append(len(data_structure))
                    else:
                        raise Exception("Invalid type for length")
                    self.ip += 1
                case I.FIND():
                    data_structure = self.data.pop()
                    if isinstance(data_structure, list | str):
                        index = int(self.data.pop())
                        if(index > len(data_structure)):
                            raise Exception("Index out of bounds")
                        self.data.append(data_structure[index])
                    elif isinstance(data_structure, dict):
                        key = self.data.pop()
                        if key not in data_structure.keys():
                            raise Exception("Key not found")
                        self.data.append(data_structure[key])
                    else:
                        raise Exception("Invalid type for lookup")
                    self.ip += 1
                case I.PUT():
                    data_structure = self.data.pop()
                    if isinstance(data_structure, list):
                        index = int(self.data.pop())
                        if(index > len(data_structure)):
                            raise Exception("Index out of bounds")
                        data_structure[index] = self.data.pop()
                        self.data.append(data_structure)
                    elif isinstance(data_structure, dict):
                        key = self.data.pop()
                        data_structure[key] = self.data.pop()
                        self.data.append(data_structure)
                    elif isinstance(data_structure, str):
                        index = int(self.data.pop())
                        if(index > len(data_structure)):
                            raise Exception("Index out of bounds")
                        data_structure = data_structure[:index] + \
                            self.data.pop() + data_structure[index+1:]
                        self.data.append(data_structure)
                    else:
                        raise Exception("Invalid type for lookup")
                    self.ip += 1

                case I.HALT():
                    if(len(self.data) == 0):
                        return None
                    return self.data.pop()


def codegen(program: AST) -> ByteCode:
    code = ByteCode()
    do_codegen(program, code)
    code.emit(I.HALT())
    return code


def do_codegen(
        program: AST,
        code: ByteCode
) -> None:
    def codegen_(program):
        do_codegen(program, code)

    simple_ops = {
        "+": I.ADD(),
        "-": I.SUB(),
        "*": I.MUL(),
        "^": I.EXP(),
        "/": I.DIV(),
        "//": I.QUOT(),
        "%": I.REM(),
        "<": I.LT(),
        ">": I.GT(),
        "<=": I.LE(),
        ">=": I.GE(),
        "==": I.EQ(),
        "!=": I.NEQ(),
        "!": I.NOT()
    }

    match program:
        case numeric_literal(what) | bool_literal(what) | string_literal(what):
            code.emit(I.PUSH(what))
        case Lists(what):
            for i in what:
                codegen_(i)
            code.emit(I.PUSH(len(what)))
            code.emit(I.BUILD_LIST())
        case dict_literal(what):
            for i in what:
                codegen_(i[0])
                codegen_(i[1])
            code.emit(I.PUSH(len(what)))
            code.emit(I.BUILD_DICT())
        case update_string(e, what):
            code.emit(I.PUSH(what))
            code.emit(I.STORE(e.variable.name))
        # case UnitLiteral():
        #     code.emit(I.PUSH(None))
        case binary_operation(op, left, right) if op in simple_ops:
            codegen_(left)
            codegen_(right)
            code.emit(simple_ops[op])
        case binary_operation("and" | "&&", left, right):
            E = code.label()
            codegen_(left)
            code.emit(I.DUP())
            code.emit(I.JMP_IF_FALSE(E))
            code.emit(I.POP())
            codegen_(right)
            code.emit_label(E)
        case binary_operation("or" | "||", left, right):
            E = code.label()
            codegen_(left)
            code.emit(I.DUP())
            code.emit(I.JMP_IF_TRUE(E))
            code.emit(I.POP())
            codegen_(right)
            code.emit_label(E)
        case unary_operation("-", operand):
            codegen_(operand)
            code.emit(I.UMINUS())
        case unary_operation("!", operand):
            codegen_(operand)
            code.emit(I.NOT())
        case block(things):
            for thing in things:
                codegen_(thing)
        case if_statement(cond, iftrue, iffalse):
            E = code.label()
            F = code.label()
            codegen_(cond)
            code.emit(I.JMP_IF_FALSE(F))
            codegen_(iftrue)
            code.emit(I.JMP(E))
            code.emit_label(F)
            codegen_(iffalse)
            code.emit_label(E)
        case while_loop(cond, body):
            B = code.label()
            E = code.label()
            code.emit_label(B)
            codegen_(cond)
            code.emit(I.JMP_IF_FALSE(E))
            codegen_(body)
            code.emit(I.JMP(B))
            code.emit_label(E)
        case string_concat(string_list):
            for i in range(len(string_list) - 1, -1, -1):
                codegen_(string_list[i])
            code.emit(I.STRCAT(len(string_list)))
        case string_slice(string, start, stop, hop):
            codegen_(string)
            codegen_(start)
            codegen_(stop)
            codegen_(hop)
            code.emit(I.STRSLICE())

        # case identifier(name) as i:
        #     code.emit(I.LOAD(i.id))

        # recheck below cases
        case let_var() as i:
            code.emit(I.LOAD(i.id))
        # case let(let_var as i, e1, e2):
        #     codegen_(e1)
        #     code.emit(I.STORE(i.localID))
        #     codegen_(e2)

        case get(identifier as i):
            code.emit(I.LOAD(i.id))

        case set(identifier as i, e):
            codegen_(e)
            code.emit(I.STORE(i.id))

        case declare(identifier as i, e):
            codegen_(e)
            code.emit(I.STORE(i.id))

        case print_statement() as i:
            for exp in i.exps:
                codegen_(exp)
                code.emit(I.PRINT())

        case list_initializer(size, val):
            codegen_(size)
            codegen_(val)
            code.emit(I.INIT_LIST())

        case u_list_operation("head", l):
            codegen_(l)
            code.emit(I.LIST_HEAD())
        case u_list_operation("tail", l):
            codegen_(l)
            code.emit(I.LIST_TAIL())
        case u_list_operation("is_empty", l):
            codegen_(l)
            code.emit(I.LIST_EMPTY())

        # We might need to add the I.STORE() instruction in these cases
        # Might not as the parser will wrap it in set() or declare()
        case b_list_operation("cons", e, l):
            codegen_(e)
            codegen_(l)
            code.emit(I.LIST_CONS())
        case b_list_operation("append", e, l):
            codegen_(e)
            codegen_(l)
            code.emit(I.LIST_APPEND())

        case u_dict_operation("keys", dict):
            codegen_(get(dict))
            code.emit(I.DICT_KEYS())
        case u_dict_operation("values", dict):
            codegen_(get(dict))
            code.emit(I.DICT_VALUES())
        case u_dict_operation("items", dict):
            codegen_(get(dict))
            code.emit(I.DICT_ITEMS())
        case b_dict_operation("delete", dict, key):
            codegen_(get(dict))
            codegen_(key)
            code.emit(I.DICT_DELETE())
            code.emit(I.STORE(dict.id))

        case length(x):
            codegen_(x)
            code.emit(I.LENGTH())
        case find(x, index):
            codegen_(index)
            codegen_(x)
            code.emit(I.FIND())
        case put(x, index, val):
            codegen_(val)
            codegen_(index)
            codegen_(x)
            code.emit(I.PUT())
            if(isinstance(x, get)):
                code.emit(I.STORE(x.variable.id))
            # This does not make sense as we only execute our AST once, so
            # we won't have the value of x in the global environment
            # if(isinstance(x, get) and isinstance(global_environment[x.variable.id], str)):
            #     code.emit(I.STORE(x.variable.id))

        # case (Variable() as v) | unary_operation("!", Variable() as v):
        #     code.emit(I.LOAD(v.localID))
        # case Put(Variable() as v, e):
        #     codegen_(e)
        #     code.emit(I.STORE(v.localID))
        # case let(Variable() as v, e1, e2) | let_var(Variable() as v, e1, e2):
        #     codegen_(e1)
        #     code.emit(I.STORE(v.localID))
        #     codegen_(e2)
        # case TypeAssertion(expr, _):
        #     codegen_(expr)
        case Function(fv, parameters, body, return_exp):
            codebegin = code.label()
            fnbegin = code.label()
            code.emit(I.JMP(codebegin))
            code.emit_label(fnbegin)
            for param in reversed(parameters):
                code.emit(I.STORE(param.id))
            codegen_(body)
            codegen_(return_exp)
            code.emit(I.RETURN())
            code.emit_label(codebegin)
            code.emit(I.PUSHFN(fnbegin))
            code.emit(I.STORE(fv.id))

        case FunctionCall(fn, args):
            for arg in args:
                codegen_(arg)
            code.emit(I.LOAD(fn.id))
            code.emit(I.CALL())


def compile(program):
    return codegen(program)


def print_bytecode(code: ByteCode):
    for i, op in enumerate(code.insns):
        match op:
            case I.JMP(Label(offset)) | I.JMP_IF_TRUE(Label(offset)) | I.JMP_IF_FALSE(Label(offset)):
                print(f"{i:=4} {op.__class__.__name__:<15} {offset}")
            case I.LOAD(localID) | I.STORE(localID):
                print(f"{i:=4} {op.__class__.__name__:<15} {localID}")
            case I.PUSH(value):
                print(f"{i:=4} {'PUSH':<15} {value}")
            case I.PUSHFN(Label(offset)):
                print(f"{i:=4} {'PUSHFN':<15} {offset}")
            case _:
                print(f"{i:=4} {op.__class__.__name__:<15}")
