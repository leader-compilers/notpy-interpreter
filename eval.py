from typing import List
from dataclasses import dataclass
from fractions import Fraction
from typing import Union, Optional, NewType



currentID = 0


def fresh():
    global currentID
    currentID = currentID + 1
    return currentID


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


@dataclass
class Null():
    type: NoneType = NoneType()
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

@dataclass
class Lists:
    value: List["AST"]


@dataclass
class dict_literal:
    value: dict["AST", "AST"]
    
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


@dataclass
class u_list_operation:
    operator: str
    first: "AST"


@dataclass
class b_list_operation:
    operator: str
    first: "AST"
    second: "AST"

@dataclass
class u_dict_operation:
    operator: str
    first: "AST"

@dataclass
class b_dict_operation:
    operator: str
    first: "AST"
    second: "AST"


@dataclass
class length:
    operand: "AST"

@dataclass
class find:
    operand: "AST"
    key: "AST"

@dataclass
class put:
    operand: "AST"
    key: "AST"
    value: "AST"


# String operation (Can take variable number of strings depending on the operation)


@dataclass
class string_concat:
    operands: List["AST"]
    type: StringType = StringType()


@dataclass
class string_slice:
    string: "AST"
    start: "AST"
    stop: "AST"
    hop: "AST" = numeric_literal(1)
    type: StringType = StringType()


# Let Expressions
@dataclass
class let_var:
    name: str
    id: int
    type: Optional[Union[NumType, BoolType, StringType, NoneType]] = None

    def make(name):
        return let_var(name, fresh())

# variables


@dataclass
class let:
    variable: let_var
    e1: "AST"
    e2: "AST"
    type: Optional[Union[NumType, BoolType, StringType, NoneType]] = None


@dataclass
class identifier:
    name: str
    id: int
    type: Optional[Union[NumType, BoolType, StringType, NoneType]] = None

    def make(name):
        return identifier(name, fresh())

@dataclass
class list_initializer:
    size: "AST"
    value: "AST"

@dataclass
class declare:
    variable: identifier
    value: "AST"
    type: Optional[Union[NumType, BoolType, StringType, NoneType]] = None


@dataclass 
class declare_list:
    variable: identifier
    size: "AST"
    value: "AST"
    # type: Optional[Union[NumType, BoolType, StringType, NoneType]] = None


@dataclass
class get:
    variable: identifier
    type: Optional[Union[NumType, BoolType, StringType, NoneType]] = None


@dataclass
class set:
    variable: identifier
    value: "AST"
    type: Optional[Union[NumType, BoolType, StringType, NoneType]] = None

@dataclass
class update_list:
    varaible: identifier
    value: List
    # type: Optional[Union[NumType, BoolType, StringType, NoneType]] = None

@dataclass
class update_dict:
    varaible: identifier
    value: dict
    # type: Optional[Union[NumType, BoolType, StringType, NoneType]] = None

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
    iterator: identifier
    initial_value: "AST"
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

# Functions
@dataclass
class Function:
    name: identifier
    parameters: List[identifier]
    body: 'AST'
    return_exp: 'AST'
    type: Optional[Union[NumType, BoolType, StringType, NoneType]] = None


@dataclass
class FunctionCall:
    function: identifier
    arguments: List['AST']
    type: Optional[Union[NumType, BoolType, StringType, NoneType]] = None


@dataclass  # to keep track of the function name and its parameters in our environment
class FunctionObject:
    parameters: List['AST']
    body: 'AST'
    return_exp: 'AST'


AST =  put | find | length | b_dict_operation | u_dict_operation | update_dict | dict_literal | update_list | declare_list | b_list_operation | u_list_operation | Lists | print_statement | for_loop | unary_operation | numeric_literal | string_literal | string_concat | string_slice | binary_operation | let | let_var | bool_literal | if_statement | while_loop | block | identifier | get | set | declare | Function | FunctionCall | Null

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

        case Null():
            return 0
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
        
        case declare_list(variable, size, value):
            size = int(eval_ast(size, lexical_scope, name_space))
            value = eval_ast(value, lexical_scope, name_space)
            l = []
            for i in range(size):
                l.append(value)
            name_space.add_to_scope(variable.name, l)
            return 0

        # eval_ast might never get this node as we are using get, however, it is still here for completeness
        case identifier(name):
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
        
        case update_list(variable, value):
            name_space.update_scope(variable.name, value)
            return Fraction(0)
        case update_dict(variable, value):
            name_space.update_scope(variable.name, value)
            return Fraction(0)

        # Literals
        case numeric_literal(value):
            return value
        case bool_literal(value):
            return value
        case string_literal(value):
            return value
        case Lists(value):
            output_list = [0 for i in range (int(eval_ast(value[0], lexical_scope, name_space)))]
            # for i in range(len(value)):
            #     output_list.append(
            #         eval_ast(value[i], lexical_scope, name_space))
            return output_list
        case dict_literal(value):
            output_dict = {}
            for i in range(len(value)):
                output_dict[eval_ast(value[i][0], lexical_scope, name_space)] = eval_ast(
                    value[i][1], lexical_scope, name_space)
            return output_dict

        # Arithmetic Operations
        case binary_operation("+", left, right):
            return Fraction(eval_ast(left, lexical_scope, name_space) + eval_ast(right, lexical_scope, name_space))
        case binary_operation("-", left, right):
            return Fraction(eval_ast(left, lexical_scope, name_space) - eval_ast(right, lexical_scope, name_space))
        case binary_operation("*", left, right):
            return Fraction(eval_ast(left, lexical_scope, name_space) * eval_ast(right, lexical_scope, name_space))
        case binary_operation("/", left, right):
            if eval_ast(right, lexical_scope, name_space) == 0:
                raise Exception("Division by zero")
            return Fraction(eval_ast(left, lexical_scope, name_space) / eval_ast(right, lexical_scope, name_space))
        case binary_operation("^", left, right):
            return Fraction(eval_ast(left, lexical_scope, name_space) ** eval_ast(right, lexical_scope, name_space))
        case binary_operation("%", left, right):
            return Fraction(eval_ast(left, lexical_scope, name_space) % eval_ast(right, lexical_scope, name_space))
        case binary_operation("//", left, right):
            return Fraction(eval_ast(left, lexical_scope, name_space) // eval_ast(right, lexical_scope, name_space))

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
        case binary_operation("or", left, right):
            return bool(eval_ast(left, lexical_scope, name_space) or eval_ast(right, lexical_scope, name_space))
        case binary_operation("and", left, right):
            return bool(eval_ast(left, lexical_scope, name_space) and eval_ast(right, lexical_scope, name_space))

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
        # using scoping as used in c++, inside loops.
        case block(exps):
            # if value of declared variables is changed inside the block, it will be changed outside the block
            # if new variables are declared inside the block, they will not be accessible outside the block
            name_space.start_scope()
            for exp in exps:
                eval_ast(exp, lexical_scope, name_space)
            name_space.end_scope()
            return Fraction(0)  # return value of block is always 0

        # Unary Operations
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

        # For loops
        case for_loop(iterator, initial_value, condition, updation, body):
            name_space.start_scope()
            eval_ast(declare(iterator, initial_value),
                     lexical_scope, name_space)
            while eval_ast(condition, lexical_scope, name_space):
                eval_ast(body, lexical_scope, name_space)
                eval_ast(updation, lexical_scope, name_space)
            name_space.end_scope()
            return Fraction(0)

        # Print statements
        case print_statement(expr_list):
            return_val = ""
            for expr in expr_list:
                value = eval_ast(expr, lexical_scope, name_space)
                return_val += str(value)
                print(value, end=" ")
            print("")
            return return_val

        # Functions
        case Function(identifier(name), parameters, body, return_exp):
            name_space.add_to_scope(
                name, FunctionObject(parameters, body, return_exp))
            return 0

        case FunctionCall(identifier(name), arguments):
            function = name_space.get_from_scope(name)
            argv = []
            for arg in arguments:
                argv.append(eval_ast(arg, lexical_scope, name_space))
            name_space.start_scope()
            for parameter, arg in zip(function.parameters, argv):
                name_space.add_to_scope(parameter.name, arg)
            for exp in function.body.exps:
                eval_ast(exp, lexical_scope, name_space)
            return_value = eval_ast(
                function.return_exp, lexical_scope, name_space)
            name_space.end_scope()
            return return_value

        case u_list_operation("self", left):
            return eval_ast(left, lexical_scope, name_space)
        case u_list_operation("head", l):
            our_list = eval_ast(get(l), lexical_scope, name_space)
            if(len(our_list) == 0):
                return Null
            return our_list[0]
        case u_list_operation("tail", l):
            our_list = eval_ast(get(l), lexical_scope, name_space)
            return our_list[1:]
        case u_list_operation("is_empty", l):
            our_list = eval_ast(get(l), lexical_scope, name_space)
            if(len(our_list) == 0):
                return True
            return False

        case b_list_operation("cons", left, l):
            our_list = eval_ast(get(l), lexical_scope, name_space)
            output_list = []
            value = eval_ast(left, lexical_scope, name_space)
            output_list.append(value)
            for i in range(len(our_list)):
                output_list.append(our_list[i])
            eval_ast(update_list(l, output_list), lexical_scope, name_space)
            return output_list
        

        case u_dict_operation("keys", d):
            our_dict = eval_ast(get(d), lexical_scope, name_space)
            return list(our_dict.keys())
        case u_dict_operation("values", d):
            our_dict = eval_ast(get(d), lexical_scope, name_space)
            return list(our_dict.values())
        case u_dict_operation("items", d):
            our_dict = eval_ast(get(d), lexical_scope, name_space)
            return list(our_dict.items())
        case b_dict_operation("delete", d, key):
            our_dict = eval_ast(get(d), lexical_scope, name_space)
            key = eval_ast(key, lexical_scope, name_space)
            del our_dict[key]
            eval_ast(update_dict(d, our_dict), lexical_scope, name_space)
            return our_dict
        
        
        case length(first):
            data_structure = eval_ast(get(first), lexical_scope, name_space)
            if isinstance(data_structure, List) or isinstance(data_structure, dict):
                return len(data_structure)
            else:
                raise Exception("Invalid type for length")
        case find(first, second):
            data_structure = eval_ast(get(first), lexical_scope, name_space)
            if isinstance(data_structure, List):
                index = int(eval_ast(second, lexical_scope, name_space))
                if(index > len(data_structure)):
                    raise Exception("Index out of bounds")
            elif isinstance(data_structure, dict):
                index = eval_ast(second, lexical_scope, name_space)
                if index not in data_structure:
                    raise Exception("Key not in dictionary")
            else: 
                raise Exception("Type does not support lookup")
            return data_structure[index]
        case put(first, second, third):
            data_structure = eval_ast(get(first), lexical_scope, name_space)
            if isinstance(data_structure, List):
                index = int(eval_ast(second, lexical_scope, name_space))
                if(index > len(data_structure)):
                    raise Exception("Index out of bounds")
                value = eval_ast(third, lexical_scope, name_space)
                data_structure[index] = value
                eval_ast(update_list(first, data_structure), lexical_scope, name_space)
                return data_structure
            elif isinstance(data_structure, dict):
                index = eval_ast(second, lexical_scope, name_space)
                value = eval_ast(third, lexical_scope, name_space)
                data_structure[index] = value
                eval_ast(update_dict(first, data_structure), lexical_scope, name_space)
                return data_structure
            else: 
                raise Exception("Type does not support lookup")
                

    # print(subprogram)
    ProgramNotSupported()
    return Fraction(0)

# Tests

# basic arithmetic

def test19():
    name_space = environment()

    ## Tests for length
    l = identifier.make("l")
    e1 = Lists([numeric_literal(1), numeric_literal(2), numeric_literal(3)])
    eval_ast(declare(l, e1), None, name_space)

    d = identifier.make("d")
    e2 = dict_literal([(string_literal("a"), numeric_literal(1)), (string_literal("b"), numeric_literal(2))])
    eval_ast(declare(d, e2), None, name_space)

    x = identifier.make("x")
    e3 = numeric_literal(0)
    eval_ast(declare(x, e3), None, name_space)

    assert(eval_ast(length(l), None, name_space) == 3)
    assert(eval_ast(length(d), None, name_space) == 2)
    # eval_ast(length(x), None, name_space)

    ## Tests for find
    for i in range(3):
        e3 = find(l, numeric_literal(i))
        assert(eval_ast(e3, None, name_space) == i + 1)
    
    for i in range(2):
        e4 = find(d, string_literal(["a", "b"][i]))
        assert(eval_ast(e4, None, name_space) == i + 1)
    # eval_ast(find(x, numeric_literal(10)), None, name_space)

    ## Tests for put
    for i in range(3):
        e5 = put(l, numeric_literal(i), numeric_literal(4))
        eval_ast(e5, None, name_space)
    assert(eval_ast(get(l), None, name_space) == [4, 4, 4])

    assert(eval_ast(put(d, string_literal("a"), numeric_literal(4)), None, name_space) == {"a": 4, "b": 2})
    assert(eval_ast(put(d, string_literal("c"), numeric_literal(5)), None, name_space) == {"a": 4, "b": 2, "c": 5})
    assert(eval_ast(length(d), None, name_space) == 3)



def test():
    name_space = environment()
    e1 = bool_literal(True)
    i = identifier("x")
    eval_ast(declare(i, e1), None, name_space)
    assert(eval_ast(binary_operation(
        "==", i, bool_literal(True)), None, name_space) == True)

#test()

def test1():
    e1 = numeric_literal(4)
    e2 = numeric_literal(5)
    e3 = numeric_literal(10)
    e4 = numeric_literal(5)
    e5 = binary_operation("+", e2, e3)
    e6 = binary_operation("/", e5, e4)
    e7 = binary_operation("*", e1, e6)
    e9 = numeric_literal(7)
    e8 = binary_operation("/", e7, e9)
    assert eval_ast(e8) == Fraction(12, 7)


def test2():
    e1 = numeric_literal(4)
    e2 = numeric_literal(5)
    e3 = numeric_literal(10)
    e4 = numeric_literal(5)
    e5 = binary_operation("^", e2, e1)
    e6 = binary_operation("*", e3, e4)
    e7 = binary_operation("/", e5, e6)
    assert eval_ast(e7) == Fraction(625, 50)


# let expressions
def test3():
    x = let_var("x")
    y = let_var("y")
    e2 = let(y, numeric_literal(3), binary_operation(
        "+", y, numeric_literal(5)))
    eval_ast(e2)
    e = let(x, numeric_literal(4), let(x, binary_operation(
        "+", x, numeric_literal(5)), binary_operation("*", x, numeric_literal(3))))
    assert eval_ast(e) == Fraction(27)


# if statements
def test4():
    e1 = numeric_literal(4)
    e2 = numeric_literal(5)
    condition = binary_operation("<", e1, e2)
    if_exp = numeric_literal(40)
    else_exp = numeric_literal(50)
    e = if_statement(condition, if_exp, else_exp)
    assert eval_ast(e) == 40


def test5():
    l1: List["AST"] = []
    e1 = numeric_literal(4)
    e2 = numeric_literal(5)
    e3 = binary_operation("+", e1, e2)
    l1.append(e1)
    l1.append(e2)
    l1.append(e3)
    b1 = block(l1)
    assert eval_ast(b1) == 0


# factorial funciton
def test6():
    name_space = environment()
    i = identifier("i")
    j = identifier("j")
    eval_ast(declare(i, numeric_literal(0)), None, name_space)
    eval_ast(declare(j, numeric_literal(0)), None, name_space)
    eval_ast(set(i, numeric_literal(1)), None, name_space)
    eval_ast(set(j, numeric_literal(1)), None, name_space)
    condition = binary_operation("<", get(i), numeric_literal(10))
    b1 = set(i, binary_operation("+", get(i), numeric_literal(1)))
    b2 = set(j, binary_operation("*", get(j), get(i)))
    body = block([b1, b2])
    e = while_loop(condition, body)
    assert eval_ast(e, None, name_space) == 0
    assert eval_ast(get(j), None, name_space) == 3628800


def test7():
    name_space = environment()  # initalising namespace
    eval_ast(numeric_literal(0), None, name_space)
    i = identifier("x")
    eval_ast(declare(i, numeric_literal(0)), None, name_space)
    eval_ast(set(i, numeric_literal(1)), None, name_space)
    assert (eval_ast(get(i), None, name_space)) == 1


def test8():
    e1 = []
    for i in range(4):
        e1.append(string_literal(str(i)))
    e2 = string_concat(e1)
    assert eval_ast(e2) == "0123"

    words = ["This", "Is", "A", "Test", "For", " ", "Concatenation"]
    e3 = []
    for i in words:
        e3.append(string_literal(i))
    e4 = string_concat(e3)
    assert eval_ast(e4) == "ThisIsATestFor Concatenation"


def test9():
    e1 = string_literal("HelloWorld")
    minusone = numeric_literal(-1)
    zero = numeric_literal(0)
    one = numeric_literal(1)
    two = numeric_literal(2)
    four = numeric_literal(4)
    ten = numeric_literal(10)
    e2 = string_slice(e1, zero, four, one)
    assert eval_ast(e2) == "Hell"
    e3 = string_slice(e1, zero, ten, two)
    assert eval_ast(e3) == "Hlool"
    e4 = string_slice(e1, four, zero, minusone)
    assert eval_ast(e4) == "olle"


def test10():
    e1 = numeric_literal(1)
    e2 = numeric_literal(1)
    e3 = unary_operation("!", binary_operation("==", e1, e2))
    assert eval_ast(e3) == False

    e1 = numeric_literal(1)
    e2 = numeric_literal(0)
    e3 = unary_operation("!", binary_operation("==", e1, e2))
    assert eval_ast(e3) == True

    e1 = string_literal("Hello")
    e2 = string_literal("Hello")
    e3 = unary_operation("!", binary_operation("==", e1, e2))
    assert eval_ast(e3) == False


def test11():
    e1 = numeric_literal(1)
    e2 = unary_operation("-", e1)
    assert eval_ast(e2) == -1

    e1 = numeric_literal(-1)
    e2 = unary_operation("-", e1)
    assert eval_ast(e2) == 1


def test12():  # For loop
    name_space = environment()

    iterator = identifier("i")
    var = identifier("var")
    last_iterator = identifier("last_iterator")

    #eval_ast(declare(iterator, numeric_literal(0)), None, name_space)
    eval_ast(declare(var, numeric_literal(0)), None, name_space)
    eval_ast(declare(last_iterator, numeric_literal(0)), None, name_space)

    condition = binary_operation("<", get(iterator), numeric_literal(5))
    updation = set(iterator, binary_operation(
        "+", get(iterator), numeric_literal(1)))

    b1 = set(var, binary_operation("+", get(var), numeric_literal(1)))
    b2 = set(last_iterator, get(iterator))
    body = block([b1, b2])

    e1 = for_loop(iterator, numeric_literal(0), condition, updation, body)
    assert eval_ast(e1, None, name_space) == 0
    assert eval_ast(get(var), None, name_space) == 5
    assert eval_ast(get(last_iterator), None, name_space) == 4


def test13():
    # checking working of enviroment for different scopes
    name_space = environment()
    i = identifier("i")
    eval_ast(declare(i, numeric_literal(0)), None, name_space)
    b1 = declare(i, numeric_literal(1))
    b2 = declare(i, numeric_literal(2))
    b11 = set(i, numeric_literal(10))

    body = block([b1, b11, b11])
    body2 = block([b2])
    eval_ast(body, None, name_space)
    eval_ast(body2, None, name_space)
    assert eval_ast(get(i), None, name_space) == 0


def test14():  # Test for print
    name_space = environment()
    e1 = numeric_literal(1)
    e2 = numeric_literal(2)
    e3 = string_literal("Hello")
    e4 = string_literal("World")
    e5 = bool_literal(True)
    e6 = identifier("i")
    eval_ast(declare(e6, numeric_literal(0)), None, name_space)
    e7 = binary_operation("+", e1, e2)
    e8 = string_concat([e3, e4])

    assert(eval_ast(print_statement([e1]), None, name_space) == "1")
    assert(eval_ast(print_statement([e3]), None, name_space) == "Hello")
    assert(eval_ast(print_statement([e5]), None, name_space) == "True")
    assert(eval_ast(print_statement([e7]), None, name_space) == "3")
    assert(eval_ast(print_statement([e8]), None, name_space) == "HelloWorld")
    assert(eval_ast(print_statement(
        [e1, e2, e3, e4, e5, e6]), None, name_space) == "12HelloWorldTrue0")


def test15():
    name_space = environment()
    x = identifier.make("x")
    e1 = Lists([numeric_literal(1), numeric_literal(2), numeric_literal(3)])
    eval_ast(declare(x, e1), None, name_space)
    e2 = get(x)
    assert(eval_ast(e2, None, name_space) == [1, 2, 3])

    y = identifier.make("y")
    eval_ast(declare(y, numeric_literal(4)), None, name_space)
    eval_ast(set(y, e1), None, name_space)
    assert(eval_ast(get(y), None, name_space) == [1, 2, 3])

    ## Initlializing list ot test list operations
    l = identifier.make("l")
    e3 = Lists([numeric_literal(1), numeric_literal(2), numeric_literal(3)])
    eval_ast(declare(l, e3), None, name_space)

    ## Tests for Head
    e4 = u_list_operation("head", l)
    assert(eval_ast(e4, None, name_space) == 1)

    ## Tests for Tail
    e5 = u_list_operation("tail", l)
    assert(eval_ast(e5, None, name_space) == [2, 3])

    ## Tests for Is_Empty
    e6 = u_list_operation("is_empty", l)
    assert(eval_ast(e6, None, name_space) == False)

    ## Tests for Cons
    e7 = b_list_operation("cons", numeric_literal(0), l)
    assert(eval_ast(e7, None, name_space) == [0, 1, 2, 3])


    ## Tests for Find
    for i in range(4):
        e4 = find(l, numeric_literal(i))    
        assert(eval_ast(e4, None, name_space) == i)

    ## Tests for Set
    for i in range(4):
        e5 = put(l, numeric_literal(i), numeric_literal(4))
        eval_ast(e5, None, name_space)
    assert(eval_ast(get(l), None, name_space) == [4, 4, 4, 4])


    ## Tests for declare list
    L = identifier.make("L")
    e1 = declare_list(L, numeric_literal(5), numeric_literal(0))
    eval_ast(e1, None, name_space)
    assert(eval_ast(get(L), None, name_space) == [0, 0, 0, 0, 0])

    e5 = put(L, numeric_literal(2), numeric_literal(4))
    assert(eval_ast(e5, None, name_space) == [0, 0, 4, 0, 0])

    e6 = length(L)
    assert(eval_ast(e6, None, name_space) == 5)


def test16():
    name_space = environment()
    i = identifier.make("i")
    j = identifier.make("j")
    fn = identifier.make("fn")
    e = Function(
        fn, [i, j], block([]), binary_operation("+", get(i), get(j)))
    eval_ast(e, None, name_space)
    program = binary_operation("+", FunctionCall(fn, [numeric_literal(15), numeric_literal(2)]),
                               FunctionCall(
                                   fn, [numeric_literal(12), numeric_literal(3)])
                               )

    assert eval_ast(program, None, name_space) == (15+2)+(12+3)


def test17():
    name_space = environment()
    i = identifier("i")
    j = identifier("j")
    fn = identifier("fn")
    e = Function(
        fn, [i, j], block([declare(identifier("test"), numeric_literal(0)), set(identifier("test"), binary_operation("^", get(i), get(j)))]), get(identifier("test")))
    eval_ast(e, None, name_space)
    program = binary_operation("+", FunctionCall(fn, [numeric_literal(15), numeric_literal(2)]),
                               FunctionCall(
                                   fn, [numeric_literal(12), numeric_literal(3)])
                               )

    assert eval_ast(program, None, name_space) == (15**2)+(12**3)


def test18():
    name_space = environment()
    d = identifier.make("d")
    e1 = dict_literal([(string_literal("a"), numeric_literal(1)), (string_literal("b"), numeric_literal(2))])
    eval_ast(declare(d, e1), None, name_space)

    ## Testing u_dict_operation
    assert(eval_ast(get(d), None, name_space) == {"a": 1, "b": 2})
    assert(eval_ast(length(d), None, name_space) == 2)
    assert(eval_ast(u_dict_operation("keys", d), None, name_space) == ["a", "b"])
    assert(eval_ast(u_dict_operation("values", d), None, name_space) == [1, 2])
    assert(eval_ast(u_dict_operation("items", d), None, name_space) == [("a", 1), ("b", 2)])


    ## Testing b_dict_operation
    assert(eval_ast(find(d, string_literal("a")), None, name_space) == 1)
    assert(eval_ast(find(d, string_literal("b")), None, name_space) == 2)
    assert(eval_ast(b_dict_operation("delete", d, string_literal("a")), None, name_space) == {"b": 2})
    assert(eval_ast(b_dict_operation("delete", d, string_literal("b")), None, name_space) == {})



def test0():
    name_space = environment()
    e1 = numeric_literal(111)
    e2 = numeric_literal(10)
    e3 = binary_operation("//", e1, e2)
    assert(eval_ast(e3, None, name_space) == 11)


# test0()
# test1()
# test2()
# test3()
# test4()
# test5()
# test6()
# test7()
# test8()
# test9()
# test10()
# test11()
# test12()
# test13()
# test14()
# test15()
# # test16()
# #test17()
# test18()
# test19()
