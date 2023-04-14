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


# class Frame:
#     locals: List[Value]

#     def __init__(self):
#         MAX_LOCALS = 32
#         self.locals = [None] * MAX_LOCALS

#global environment
global_environment : dict[int:'Value']= {}

class VM:
    bytecode: ByteCode
    ip: int
    data: List[Value]
    #currentFrame: Frame

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
                    #the data would be loaded from the current frame
                    #if none then error
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
                  
                    #self.currentFrame.locals[localID] = v
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
        
        case identifier() as i:
            code.emit(I.LOAD(i.id))

        #recheck below cases
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
        
        case print_statement(exps):
            for exp in exps:
                codegen_(exp)
                code.emit(I.PRINT())

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
