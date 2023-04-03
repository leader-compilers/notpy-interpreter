from dataclasses import dataclass
from fractions import Fraction
from typing import Union, MutableMapping, List, TypeVar, Optional

@dataclass
class Null():
    pass

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
    operands: List["AST"]


@dataclass
class string_slice:
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
class identifier:
    name: str


@dataclass
class declare:
    variable: identifier
    value: "AST"


@dataclass
class get:
    variable: identifier


@dataclass
class set:
    variable: identifier
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
    iterator: identifier
    initial_value: "AST"
    condition: "AST"
    updation: "AST"
    body: "AST"


@dataclass
class block:
    exps: List["AST"]


@dataclass
class Null:
    pass


@dataclass
class print_statement:
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

Value = Fraction | bool | str


def ProgramNotSupported():
    raise Exception(
        "Program not supported, it may be in the future versions of the language")


################################### NEW ############################################

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
        length: int

    @dataclass
    class PRINT:
        length: int

    @dataclass
    class HALT:
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
    | I.PRINT
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


class Frame:
    locals: List[Value]

    def __init__(self):
        MAX_LOCALS = 32
        self.locals = [None] * MAX_LOCALS

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
                    self.data.append(left==right)
                    self.ip += 1
                case I.NEQ():
                    right = self.data.pop()
                    left = self.data.pop()
                    self.data.append(left!=right)
                    self.ip += 1
                case I.LT():
                    right = self.data.pop()
                    left = self.data.pop()
                    self.data.append(left<right)
                    self.ip += 1
                case I.GT():
                    right = self.data.pop()
                    left = self.data.pop()
                    self.data.append(left>right)
                    self.ip += 1
                case I.LE():
                    right = self.data.pop()
                    left = self.data.pop()
                    self.data.append(left<=right)
                    self.ip += 1
                case I.GE():
                    right = self.data.pop()
                    left = self.data.pop()
                    self.data.append(left>=right)
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
                    self.data.append(self.currentFrame.locals[localID])
                    self.ip += 1
                case I.STORE(localID):
                    v = self.data.pop()
                    self.currentFrame.locals[localID] = v
                    self.ip += 1
                case I.STRCAT(size):
                    string = ""
                    for i in range(size):
                        string += self.data.pop()
                    self.data.append(string)
                    self.ip += 1
                case I.PRINT(size):
                    string = ""
                    for i in range(size):
                        s = self.data.pop()
                        string += str(s)
                        if i != size-1:
                            string += " "
                        print(s, end=" ")
                    print()
                    self.data.append(string)
                    self.ip += 1
                case I.HALT():
                    return self.data.pop()

def codegen(program: AST) -> ByteCode:
    code = ByteCode()
    do_codegen(program, code)
    code.emit(I.HALT())
    return code

def do_codegen (
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
        # "!": I.NOT()
    }


    match program:
        case numeric_literal(what) | bool_literal(what) | string_literal(what):
            code.emit(I.PUSH(what))
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
            # for string in string_list:
            for i in range(len(string_list)-1, -1,-1):
                codegen_(string_list[i])
            code.emit(I.STRCAT(len(string_list)))
        case print_statement(expr_list):
            for i in range(len(expr_list)-1, -1,-1):
                codegen_(expr_list[i])
            code.emit(I.PRINT(len(expr_list)))


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
from dataclasses import dataclass
from fractions import Fraction
from typing import Union, MutableMapping, List, TypeVar, Optional

@dataclass
class Null():
    pass

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
    operands: List["AST"]


@dataclass
class string_slice:
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
class identifier:
    name: str


@dataclass
class declare:
    variable: identifier
    value: "AST"


@dataclass
class get:
    variable: identifier


@dataclass
class set:
    variable: identifier
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
    iterator: identifier
    initial_value: "AST"
    condition: "AST"
    updation: "AST"
    body: "AST"


@dataclass
class block:
    exps: List["AST"]


@dataclass
class Null:
    pass


@dataclass
class print_statement:
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

Value = Fraction | bool | str


def ProgramNotSupported():
    raise Exception(
        "Program not supported, it may be in the future versions of the language")


################################### NEW ############################################

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


class Frame:
    locals: List[Value]

    def __init__(self):
        MAX_LOCALS = 32
        self.locals = [None] * MAX_LOCALS

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
                    self.data.append(left==right)
                    self.ip += 1
                case I.NEQ():
                    right = self.data.pop()
                    left = self.data.pop()
                    self.data.append(left!=right)
                    self.ip += 1
                case I.LT():
                    right = self.data.pop()
                    left = self.data.pop()
                    self.data.append(left<right)
                    self.ip += 1
                case I.GT():
                    right = self.data.pop()
                    left = self.data.pop()
                    self.data.append(left>right)
                    self.ip += 1
                case I.LE():
                    right = self.data.pop()
                    left = self.data.pop()
                    self.data.append(left<=right)
                    self.ip += 1
                case I.GE():
                    right = self.data.pop()
                    left = self.data.pop()
                    self.data.append(left>=right)
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
                    self.data.append(self.currentFrame.locals[localID])
                    self.ip += 1
                case I.STORE(localID):
                    v = self.data.pop()
                    self.currentFrame.locals[localID] = v
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
                case I.HALT():
                    return self.data.pop()

def codegen(program: AST) -> ByteCode:
    code = ByteCode()
    do_codegen(program, code)
    code.emit(I.HALT())
    return code

def do_codegen (
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
        # "!": I.NOT()
    }


    match program:
        case numeric_literal(what) | bool_literal(what) | string_literal(what):
            code.emit(I.PUSH(what))
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

def compile(program):
    return codegen(program)

def compile(program):
    return codegen(program)