from dataclasses import dataclass
from fractions import Fraction
from typing import Union
from typing import Optional, NewType
from lexer import *
from eval import *


@dataclass
class Parser:
    tokens: lexer

    def call_parser(tokens):
        return Parser(tokens)

    def parse_primary(self):

        match self.tokens.peek_token():
            case Identifier(name):
                self.tokens.advance()
                match self.tokens.peek_token():
                    case Operator(op) if op in "=":
                        self.tokens.advance()
                        return self.parse_set(name)
                    case Operator(op) if op in "[":
                        vals = []
                        self.tokens.advance()
                        a = self.parse_logic()
                        match self.tokens.peek_token():
                            case Operator(op) if op in ":":
                                self.tokens.advance()
                                vals.append(a)
                                while True:
                                    vals.append(self.parse_logic())
                                    match self.tokens.peek_token():
                                        case Operator(op) if op in "]":
                                            self.tokens.advance()
                                            self.tokens.match(Operator(";"))
                                            break
                                        case Operator(op) if op in ":":
                                            self.tokens.advance()
                                if len(vals) == 2:
                                    return string_slice(string_literal(name), vals[0], vals[1])
                                return string_slice(string_literal(name), vals[0], vals[1], vals[2])

                        self.tokens.match(Operator("]"))
                        match self.tokens.peek_token():
                            case Operator(op) if op in "=":
                                self.tokens.advance()
                                val = self.parse_logic()
                                self.tokens.match(Operator(";"))
                                return put(get(identifier.make(name)), a, val)
                        return find(get(identifier.make(name)), a)

                    case Operator(op) if op in ".":
                        self.tokens.advance()
                        if self.tokens.peek_token().word == "head":
                            self.tokens.advance()
                            return u_list_operation("head", get(identifier.make(name)))
                        elif self.tokens.peek_token().word == "tail":
                            self.tokens.advance()
                            return u_list_operation("tail", get(identifier.make(name)))
                        elif self.tokens.peek_token().word == "empty":
                            self.tokens.advance()
                            return u_list_operation("is_empty", get(identifier.make(name)))
                        elif self.tokens.peek_token().word == "cons":
                            self.tokens.advance()
                            self.tokens.match(Operator("("))
                            match self.tokens.peek_token():
                                case Identifier(name2):
                                    a = get(identifier.make(name2))
                                case String(value):
                                    a = string_literal(value)
                                case Num(value):
                                    a = numeric_literal(value)
                            # a = numeric_literal(self.tokens.peek_token().n)
                            self.tokens.advance()
                            # print(self.tokens.peek_token())
                            self.tokens.match(Operator(")"))
                            self.tokens.match(Operator(";"))
                            return b_list_operation("cons", a, get(identifier.make(name)))
                        elif self.tokens.peek_token().word == "length":
                            self.tokens.advance()
                            return length(get(identifier.make(name)))
                        elif self.tokens.peek_token().word == "append":
                            self.tokens.advance()
                            self.tokens.match(Operator("("))
                            match self.tokens.peek_token():
                                case Identifier(name2):
                                    a = get(identifier.make(name2))
                                case String(value):
                                    a = string_literal(value)
                                case Num(value):
                                    a = numeric_literal(value)
                            self.tokens.advance()
                            self.tokens.match(Operator(")"))
                            match self.tokens.peek_token():
                                case Operator(op) if op in ";":
                                    self.tokens.advance()
                            return b_list_operation("append", a, get(identifier.make(name)))

                        elif self.tokens.peek_token().word == "keys":
                            self.tokens.advance()
                            return u_dict_operation("keys", get(identifier.make(name)))
                        elif self.tokens.peek_token().word == "values":
                            self.tokens.advance()
                            return u_dict_operation("values", get(identifier.make(name)))
                        elif self.tokens.peek_token().word == "items":
                            self.tokens.advance()
                            return u_dict_operation("items", get(identifier.make(name)))
                        elif self.tokens.peek_token().word == "iskey":
                            self.tokens.advance()
                            self.tokens.match(Operator("("))
                            # while True:
                            #     a = self.parse_logic()
                            #     if self.tokens.peek_token().word == ")":
                            #         break
                            match self.tokens.peek_token():
                                case Identifier(name2):
                                    key = get(identifier.make(name2))
                                case String(value):
                                    key = string_literal(value)
                                case Num(value):
                                    key = numeric_literal(value)
                            self.tokens.advance()
                            self.tokens.match(Operator(")"))
                            self.tokens.match(Operator(";"))
                            return b_dict_operation("iskey", get(identifier.make(name)), key)

                        elif self.tokens.peek_token().word == "delete":
                            self.tokens.advance()
                            self.tokens.match(Operator("("))
                            match self.tokens.peek_token():
                                case Identifier(name2):
                                    key = get(identifier.make(name2))
                                case String(value):
                                    key = string_literal(value)
                                case Num(value):
                                    key = numeric_literal(value)
                            self.tokens.advance()
                            self.tokens.match(Operator(")"))
                            self.tokens.match(Operator(";"))
                            return b_dict_operation("delete", get(identifier.make(name)), key)
                return get(identifier.make(name))

            case Num(value):
                self.tokens.advance()
                return numeric_literal(value)
            case boolValue(name):
                self.tokens.advance()
                return bool_literal(bool(name))
            case String(value):
                self.tokens.advance()
                # vals = []
                # match self.tokens.peek_token():
                #     case Operator(op) if op in "[":
                #         self.tokens.advance()
                #         while True:
                #             vals.append(self.parse_logic())
                #             match self.tokens.peek_token():
                #                 case Operator(op) if op in "]":
                #                     self.tokens.advance()
                #                     break
                #             self.tokens.match(Operator(":"))

                #         if len(vals) == 2:
                #             return string_slice(string_literal(value), vals[0], vals[1])
                #         return string_slice(string_literal(value), vals[0], vals[1], vals[2])
                return string_literal(value)
            case functionName(name):
                a = self.parse_function_call()
                return a

    def parse_power(self):
        left = self.parse_primary()
        while True:

            match self.tokens.peek_token():
                case Operator(op) if op in "^" or op in "**":
                    self.tokens.advance()
                    m = self.parse_power()
                    left = binary_operation(op, left, m)
                case _:
                    break

        return left

    def parse_unary(self):
        left = self.parse_power()
        while True:
            match self.tokens.peek_token():
                case Operator(op) if op in "!":
                    self.tokens.advance()
                    m = self.parse_unary()
                    left = unary_operation(op, m)
                case _:
                    break
        return left

    def parse_floor(self):
        left = self.parse_unary()
        while True:

            match self.tokens.peek_token():
                case Operator(op) if op == "//":
                    self.tokens.advance()
                    m = self.parse_floor()
                    left = binary_operation(op, left, m)
                case _:
                    break
        return left

    def parse_mult(self):
        left = self.parse_floor()
        while True:

            match self.tokens.peek_token():
                case Operator(op) if op in "*/%":
                    self.tokens.advance()
                    m = self.parse_mult()
                    left = binary_operation(op, left, m)
                case _:
                    break
        return left

    def parse_add(self):
        left = self.parse_mult()
        while True:

            match self.tokens.peek_token():

                case Operator(op) if op in "+-":
                    self.tokens.advance()
                    m = self.parse_add()
                    if left == None:
                        left = unary_operation(op, m)
                    else:
                        if isinstance(left, string_literal) and isinstance(m, string_literal):
                            left = string_concat([left.value, m.value])
                        elif isinstance(left, string_literal) and isinstance(m, string_concat):
                            left = string_concat([left.value, m])
                        elif isinstance(left, string_concat) and isinstance(m, string_concat):
                            left = string_concat([left, m])
                        else:
                            left = binary_operation(op, left, m)
                case _:
                    break
        return left

    def parse_comp(self):
        left = self.parse_add()
        match self.tokens.peek_token():
            case Operator(op) if op in "<>":
                self.tokens.advance()
                right = self.parse_add()
                return binary_operation(op, left, right)
        return left

    def parse_equal(self):
        left = self.parse_comp()
        match self.tokens.peek_token():
            case Operator(op) if op == "==" or op == "!=":
                self.tokens.advance()
                right = self.parse_comp()
                return binary_operation(op, left, right)
        return left

    def parse_logic(self):
        left = self.parse_equal()
        match self.tokens.peek_token():
            case Operator(op) if op == "and" or op == "or":
                self.tokens.advance()
                right = self.parse_equal()
                return binary_operation(op, left, right)
        return left

    def parse_set(self, name):

        while True:
            value = self.parse_expr_key()
            match self.tokens.peek_token():
                case Operator(op) if op in ";":
                    self.tokens.advance()
                    break
                case Operator(op) if op in ")":
                    break
        if not value:
            return None
        return set(identifier.make(name), value)

    def parse_expr(self):

        b = []
        match self.tokens.peek_token():
            case Operator(op) if op in "{":
                self.tokens.advance()
            # case _:
            #     raise Exception("Expected { at the start  of the program")

        while True:
            match self.tokens.peek_token():

                case Operator(op) if op in "}":
                    self.tokens.advance()
                    return block(b)

                case EndOfLine(EOL) if EOL in "EndOfLine":
                    return block(b)

                case Keyword("let"):
                    b.append(self.parse_let())

                case null("pass"):
                    b.append(self.parse_null())
                    self.tokens.match(Operator(";"))

                case Keyword("for"):
                    b.append(self.parse_for())

                case Keyword("if"):
                    b.append(self.parse_if())

                case Keyword("def"):
                    b.append(self.parse_function())

                case Keyword("while"):
                    b.append(self.parse_while())

                case Keyword("print"):
                    b.append(self.parse_print())
                    self.tokens.match(Operator(";"))

                case Keyword("list"):
                    b.append(self.parse_list_initialize())
                    self.tokens.match(Operator(";"))

                case Keyword("var"):
                    b.append(self.parse_declare())
                    self.tokens.match(Operator(";"))

                case _:
                    tree = self.parse_logic()
                    b.append(tree)
                    match self.tokens.peek_token():
                        case Operator(op) if op in ";":
                            return b[0]
                        case Operator(op) if op in ")":
                            return b[0]
                    # print(self.tokens.peek_token())

    def parse_expr_key(self):
        b = []
        while True:
            # print(self.tokens.peek_token())
            match self.tokens.peek_token():
                case EndOfLine(EOL) if EOL in "EndOfLine":
                    return b

                case Keyword("let"):
                    b.append(self.parse_let())
                    self.tokens.match(Operator(";"))
                    return b

                case null("pass"):
                    b.append(self.parse_null())
                    self.tokens.match(Operator(";"))

                case Keyword("for"):
                    b.append(self.parse_for())

                case Keyword("if"):
                    b.append(self.parse_if())

                case Keyword("def"):
                    b.append(self.parse_function())

                case Keyword("while"):
                    b.append(self.parse_while())

                case Keyword("print"):
                    b.append(self.parse_print())
                    self.tokens.match(Operator(";"))
                    return b

                case Operator("["):
                    b.append(self.parse_List())
                    return b[0]

                case Operator("{"):
                    b.append(self.parse_dict())
                    return b[0]

                case Keyword("var"):
                    b.append(self.parse_declare())
                    self.tokens.match(Operator(";"))
                    return b

                case Keyword("list"):
                    b.append(self.parse_list_initialize())
                    return b[0]

                case Keyword("input"):
                    b.append(self.parse_input())
                    return b[0]

                case _:
                    tree = self.parse_logic()
                    return tree

    def parse_expr_forloop(self):
        b = []

        while True:
            match self.tokens.peek_token():

                case Operator(op) if op in "}":
                    if len(b) == 1:
                        return b[0]
                    else:
                        return b

                case Keyword("let"):
                    b.append(self.parse_let())
                    self.tokens.match(Operator(";"))

                case null("pass"):
                    b.append(self.parse_null())
                    self.tokens.match(Operator(";"))

                case Keyword("for"):
                    b.append(self.parse_for())

                case Keyword("if"):
                    b.append(self.parse_if())

                case Keyword("def"):
                    b.append(self.parse_function())

                case Keyword("while"):
                    b.append(self.parse_while())

                case Keyword("print"):
                    b.append(self.parse_print())
                    self.tokens.match(Operator(";"))

                case Keyword("list"):
                    b.append(self.parse_list_initialize())
                    self.tokens.match(Operator(";"))

                case Keyword("var"):
                    b.append(self.parse_declare())
                    self.tokens.match(Operator(";"))

                case Operator("["):
                    b.append(self.parse_List())
                    self.tokens.match(Operator(";"))

                case Operator("{"):
                    b.append(self.parse_dict())
                    self.tokens.match(Operator(";"))

                case _:
                    tree = self.parse_logic()
                    b.append(tree)

    def parse_expr_func(self):

        b = []
        while True:
            match self.tokens.peek_token():

                case Keyword("return"):
                    return b

                case Operator(op) if op in "}":
                    self.tokens.advance()
                    return b

                case Keyword("let"):
                    b.append(self.parse_let())
                    self.tokens.match(Operator(";"))

                case null("pass"):
                    b.append(self.parse_null())
                    self.tokens.match(Operator(";"))

                case Keyword("for"):
                    b.append(self.parse_for())

                case Keyword("if"):
                    b.append(self.parse_if())

                case Keyword("def"):
                    b.append(self.parse_function())

                case Keyword("while"):
                    b.append(self.parse_while())

                case Keyword("print"):
                    b.append(self.parse_print())
                    self.tokens.match(Operator(";"))

                case Keyword("list"):
                    b.append(self.parse_list_initialize())
                    self.tokens.match(Operator(";"))

                case Keyword("var"):
                    b.append(self.parse_declare())
                    self.tokens.match(Operator(";"))

                case Operator("["):
                    b.append(self.parse_List())
                    self.tokens.match(Operator(";"))

                case Operator("{"):
                    b.append(self.parse_dict())
                    self.tokens.match(Operator(";"))

                case _:
                    b.append(self.parse_logic())
                    return b

    def parse_function_call(self):
        match self.tokens.peek_token():
            case functionName(name):
                self.tokens.advance()
                match self.tokens.peek_token():
                    case Operator("("):
                        self.tokens.advance()
                        parameters = []
                        while True:
                            parameters.append(self.parse_logic())
                            match self.tokens.peek_token():
                                case Operator(op) if op in ")":
                                    self.tokens.advance()
                                    break
                            self.tokens.match(Operator(","))

                        return FunctionCall(identifier.make(name), parameters)

                    case _:
                        raise SyntaxError("Missing '(' after function {name}")

    def parse_function(self):
        match self.tokens.peek_token():
            case Keyword("def"):
                self.tokens.advance()
                match self.tokens.peek_token():
                    case functionName(name):
                        self.tokens.advance()
                        match self.tokens.peek_token():
                            case Operator("("):
                                self.tokens.advance()
                                parameters = []
                                while self.tokens.peek_token() is not None:
                                    if isinstance(self.tokens.peek_token(), Identifier):
                                        word = self.tokens.peek_token().word
                                        parameters.append(
                                            identifier.make(word))

                                        self.tokens.advance()
                                        if isinstance(self.tokens.peek_token(), Operator) and self.tokens.peek_token().op == ")":
                                            self.tokens.advance()

                                        elif isinstance(self.tokens.peek_token(), Operator) and self.tokens.peek_token().op == "{":
                                            self.tokens.advance()
                                            break

                                        elif isinstance(self.tokens.peek_token(), Operator) and self.tokens.peek_token().op == ",":
                                            self.tokens.advance()
                                            continue
                                        else:
                                            raise SyntaxError(
                                                "Unexpected token")

                                    elif isinstance(self.tokens.peek_token(), Operator) and self.tokens.peek_token().op == "{":
                                        self.tokens.advance()
                                        break

                                    else:
                                        raise SyntaxError("Unexpected token")

                                exprs = []
                                while True:
                                    exprs.append(self.parse_expr_func())
                                    match self.tokens.peek_token():
                                        case Keyword(word) if word in "return":
                                            self.tokens.advance()
                                            ret_expr = self.parse_expr_key()
                                            break
                                    self.tokens.match(Operator(";"))

                                self.tokens.match(Operator(";"))
                                self.tokens.match(Operator("}"))
                                if type(exprs[0]) == list:
                                    body = block(exprs[0])
                                else:
                                    body = block(exprs)
                                return Function(identifier.make(name), parameters, body, ret_expr)
                            case _:
                                raise SyntaxError("Unexpected token")
                    case _:
                        raise SyntaxError("Unexpected token")
            case _:
                return None

    def parse_null(self):
        self.tokens.match(null("pass"))
        return Null()

    def parse_while(self):
        self.tokens.match(Keyword("while"))
        self.tokens.match(Operator("("))
        c = self.parse_logic()
        self.tokens.match(Operator(")"))
        self.tokens.match(Operator("{"))
        exprs = []
        while True:
            match self.tokens.peek_token():
                case Operator("}"):
                    self.tokens.advance()
                    break

            exprs.append(self.parse_expr_forloop())

        if type(exprs[0]) == list:
            b = block(exprs[0])
        else:
            b = block(exprs)
        return while_loop(c, b)

    def parse_if(self):
        self.tokens.match(Keyword("if"))
        self.tokens.match(Operator("("))
        c = self.parse_logic()
        self.tokens.match(Operator(")"))
        self.tokens.match(Operator("{"))
        exprs = []
        while True:
            match self.tokens.peek_token():
                case Operator("}"):
                    self.tokens.advance()
                    break
            exprs.append(self.parse_expr_forloop())

        if type(exprs[0]) == list:
            t = block(exprs[0])
        else:
            t = block(exprs)

            ############### elif implemented###########
        # while True:
        #     match self.tokens.peek_token():
        #         case Keyword("elif"):
        #             self.tokens.match(Keyword("elif"))
        #             self.tokens.match(Operator("{"))
        #             elifs = []
        #             while True:
        #                 match self.tokens.peek_token():
        #                     case Operator("}"):
        #                         self.tokens.advance()
        #                         break
        #                 elifs.append(self.parse_expr_forloop())
        #             g = block(elifs)

        #         case _:
        #             g = None
        #             break

        match self.tokens.peek_token():
            case Keyword("else"):
                self.tokens.advance()
                self.tokens.match(Operator("{"))
                exprs = []
                while True:
                    match self.tokens.peek_token():
                        case Operator("}"):
                            self.tokens.advance()
                            break
                    exprs.append(self.parse_expr_forloop())

                if type(exprs[0]) == list:
                    f = block(exprs[0])
                else:
                    f = block(exprs)

            case _:
                f = block([Null()])

        return if_statement(c, t, f)

    def parse_for(self):
        self.tokens.match(Keyword("for"))
        self.tokens.match(Operator("("))
        iterator = self.tokens.peek_token().word
        self.tokens.advance()
        self.tokens.match(Operator("="))
        initial_value = self.parse_expr()
        self.tokens.match(Operator(";"))
        condition = self.parse_logic()
        self.tokens.match(Operator(";"))
        increment = self.parse_expr()
        self.tokens.match(Operator(")"))
        self.tokens.match(Operator("{"))

        exprs = []
        while True:
            match self.tokens.peek_token():
                case Operator(op) if op in "}":
                    self.tokens.advance()
                    break
            exprs.append(self.parse_expr_forloop())

        if type(exprs[0]) == list:
            body = block(exprs[0])
        else:
            body = block(exprs)
        return for_loop(identifier.make(iterator), initial_value, condition, increment, body)

    def parse_input(self):
        self.tokens.match(Keyword("input"))
        self.tokens.match(Operator("("))
        string = self.tokens.peek_token().s
        self.tokens.advance()
        self.tokens.match(Operator(")"))
        return input_statement(string)

    def parse_print(self):
        self.tokens.match(Keyword("print"))
        exprs = []
        while True:
            exprs.append(self.parse_expr_key())
            match self.tokens.peek_token():
                case Operator(op) if op in ";":
                    break
            self.tokens.match(Operator(","))
        return print_statement(exprs)

    def parse_list_initialize(self):
        self.tokens.match(Keyword("list"))
        self.tokens.match(Operator("("))
        exprs = []
        while True:
            exprs.append(self.parse_logic())
            match self.tokens.peek_token():
                case Operator(op) if op in ")":
                    break
            self.tokens.match(Operator(","))
        self.tokens.match(Operator(")"))
        if exprs[0] == None:
            return list_initializer(numeric_literal(0), numeric_literal(0))

        match exprs[0]:
            case Identifier(name):
                exprs[0] = get(exprs[0])
        match exprs[1]:
            case Identifier(name):
                exprs[1] = get(exprs[1])

        return list_initializer(exprs[0], exprs[1])

    def parse_List(self):
        self.tokens.match(Operator("["))
        values = []
        while True:
            values.append(self.parse_logic())
            match self.tokens.peek_token():
                case Operator(op) if op in "]":
                    break
            self.tokens.match(Operator(","))
        self.tokens.match(Operator("]"))
        return Lists(values)

    def parse_dict(self):
        self.tokens.match(Operator("{"))
        values = []
        keys = []
        dicto = []
        i = 0
        while True:
            keys.append(self.parse_logic())
            match self.tokens.peek_token():
                case Operator(op) if op in ":":
                    self.tokens.advance()
            values.append(self.parse_logic())
            dicto.append((keys[i], values[i]))
            match self.tokens.peek_token():
                case Operator(op) if op in "}":
                    break
            self.tokens.match(Operator(","))
            i += 1
        self.tokens.match(Operator("}"))
        if dicto[0][0] == None:
            return dict_literal(([]))
        return dict_literal(dicto)

    def parse_let(self):
        self.tokens.match(Keyword("let"))
        name = self.tokens.peek_token()
        self.tokens.advance()
        self.tokens.match(Operator("="))
        value = self.parse_expr_key()
        self.tokens.match(Keyword("in"))
        body = self.parse_expr_key()
        return let(name, value, body)

    def parse_declare(self):
        self.tokens.match(Keyword("var"))
        vari = self.tokens.peek_token().word
        self.tokens.advance()
        match self.tokens.peek_token():
            case Operator(op) if op != "=":
                return None
        self.tokens.advance()  # consume the "="
        while True:
            value = self.parse_expr_key()
            match self.tokens.peek_token():
                case Operator(op) if op in ";":
                    break
        if not value:
            return None

        return declare(identifier.make(vari), value)


def test_parse0():
    def parse(string):
        return Parser.parse_expr(
            Parser.call_parser(lexer.lexerFromStream(
                Stream.streamFromString(string)))
        )

    print(parse("{var a =4; for( i = 1 ; i < 1001 ; i = i + 1){if (i%3 == 0 or i%5==0) {total = total + i;} else {total = total;} } }"))


def test_parse1():
    def parse(string):
        return Parser.parse_expr(
            Parser.call_parser(lexer.lexerFromStream(
                Stream.streamFromString(string)))
        )
    print(parse("{print 1, 2, 3;}"))
    eval_ast(parse("{print 1, 2, 3;}"), None, None)


def test_parse2():
    def parse(string):
        return Parser.parse_expr(
            Parser.call_parser(lexer.lexerFromStream(
                Stream.streamFromString(string)))
        )

    # You should parse, evaluate and see whether the expression produces the expected value in your tests.
    print(parse("{let a = 1 in a = a + 2;}"))


def test_parse3():
    def parse(string):
        return Parser.parse_expr(
            Parser.call_parser(lexer.lexerFromStream(
                Stream.streamFromString(string)))
        )
    print(parse("{ 1 or 2 }"))
    print(eval_ast(parse("{1 + 2}"), None, None))


def test_parse4():
    def parse(string):
        return Parser.parse_expr(
            Parser.call_parser(lexer.lexerFromStream(
                Stream.streamFromString(string)))
        )

    # print(parse("a+b"))
    print(parse("{6+7+8}"))
    # You should parse, evaluate and see whether the expression produces the expected value in your tests.
    print(eval_ast(parse("{6+7+8}")))


def test_parse5():
    def parse(string):
        return Parser.parse_expr(
            Parser.call_parser(lexer.lexerFromStream(
                Stream.streamFromString(string)))
        )

    # print(parse("var a = 2;"))
    # You should parse, evaluate and see whether the expression produces the expected value in your tests.
    # print(eval_ast(parse("var a = 2+3;;"),None, None))
    print(parse("{var a = 2+3; r = -1;}"))


def test_parse6():
    def parse(string):
        return Parser.parse_expr(
            Parser.call_parser(lexer.lexerFromStream(
                Stream.streamFromString(string)))
        )
    print(parse("{if(1){var j = 2;} else {p=3;}}"))


def test_parse7():
    def parse(string):
        return Parser.parse_expr(
            Parser.call_parser(lexer.lexerFromStream(
                Stream.streamFromString(string)))
        )
    print(parse("{a = w+c+d+e;}"))


def test_parse8():
    def parse(string):
        return Parser.parse_expr(
            Parser.call_parser(lexer.lexerFromStream(
                Stream.streamFromString(string)))
        )
    # print(eval_ast(parse("def fun(a, b){ a=c+d+e; i = 2; return a+b; }")))
    # print(parse("def fun(a, b){ a=c+d+e; i = 2; return a+b; }"))
    # print(parse("def fun(n){ var val = n; return val; }"))
    print(parse("{def fun(n){var val = 2; return val;} fun(0, 1)}"))


def test_parse9():
    def parse(string):
        return Parser.parse_expr(
            Parser.call_parser(lexer.lexerFromStream(
                Stream.streamFromString(string)))
        )
    print(parse("var c = fun(1); s = 1;"))


def test_parse10():
    def parse(string):
        return Parser.parse_expr(
            Parser.call_parser(lexer.lexerFromStream(
                Stream.streamFromString(string)))
        )
    print(parse("{while (i<30){i=i+1;a=a+1;}}"))


def test_parse11():
    def parse(string):
        return Parser.parse_expr(
            Parser.call_parser(lexer.lexerFromStream(
                Stream.streamFromString(string)))
        )
    print(parse("{for( i = 1 ; i < 1001 ; i = i + 1){i=1;}}"))


def test_parse12():
    def parse(string):
        return Parser.parse_expr(
            Parser.call_parser(lexer.lexerFromStream(
                Stream.streamFromString(string)))
        )
    print(parse("{ pass; }"))


def test_parse13():
    def parse(string):
        return Parser.parse_expr(
            Parser.call_parser(lexer.lexerFromStream(
                Stream.streamFromString(string)))
        )
    print(parse("{while (i<30){if(j%10==0){i=i+1;} else {i=i+2;} j = i+j;}}"))


def test_parse14():
    def parse(string):
        return Parser.parse_expr(
            Parser.call_parser(lexer.lexerFromStream(
                Stream.streamFromString(string)))
        )
    print(parse("var a  = [1,2,3];"))


def test_parse15():
    def parse(string):
        return Parser.parse_expr(
            Parser.call_parser(lexer.lexerFromStream(
                Stream.streamFromString(string)))
        )
    print(parse("a.head;"))


def test_parse16():
    def parse(string):
        return Parser.parse_expr(
            Parser.call_parser(lexer.lexerFromStream(
                Stream.streamFromString(string)))
        )
    print(parse("a.tail;"))


def test_parse17():
    def parse(string):
        return Parser.parse_expr(
            Parser.call_parser(lexer.lexerFromStream(
                Stream.streamFromString(string)))
        )
    print(parse("a.empty;"))


def test_parse18():
    def parse(string):
        return Parser.parse_expr(
            Parser.call_parser(lexer.lexerFromStream(
                Stream.streamFromString(string)))
        )
    print(parse("a.append(1);"))


def test_parse19():
    def parse(string):
        return Parser.parse_expr(
            Parser.call_parser(lexer.lexerFromStream(
                Stream.streamFromString(string)))
        )
    print(parse("a.length;"))


def test_parse20():
    def parse(string):
        return Parser.parse_expr(
            Parser.call_parser(lexer.lexerFromStream(
                Stream.streamFromString(string)))
        )
    print(parse("a[9] = 1;"))


def test_parse21():
    def parse(string):
        return Parser.parse_expr(
            Parser.call_parser(lexer.lexerFromStream(
                Stream.streamFromString(string)))
        )
    print(parse("a[9];"))


def test_parse22():
    def parse(string):
        return Parser.parse_expr(
            Parser.call_parser(lexer.lexerFromStream(
                Stream.streamFromString(string)))
        )
    string = 'var a  = {"1" :2, "7":3, "8":0};'
    # string = repr(string)
    print(parse(string))


def test_parse23():
    def parse(string):
        return Parser.parse_expr(
            Parser.call_parser(lexer.lexerFromStream(
                Stream.streamFromString(string)))
        )
    string = "a.delete(2);"
    # string = repr(string)
    print(parse(string))


def test_parse24():
    def parse(string):
        return Parser.parse_expr(
            Parser.call_parser(lexer.lexerFromStream(
                Stream.streamFromString(string)))
        )
    string = "a.items;"
    # string = repr(string)
    print(parse(string))


def test_parse25():
    def parse(string):
        return Parser.parse_expr(
            Parser.call_parser(lexer.lexerFromStream(
                Stream.streamFromString(string)))
        )
    string = "var t = list(1,2);"
    # string = repr(string)
    print(parse(string))


def test_parse26():
    def parse(string):
        return Parser.parse_expr(
            Parser.call_parser(lexer.lexerFromStream(
                Stream.streamFromString(string)))
        )
    string = "for(i=0; i<8; i=i+1) { var c = list(1,2); var j = [0, 1, 2]; }"
    # string = repr(string)
    print(parse(string))


def test_parse27():
    def parse(string):
        return Parser.parse_expr(
            Parser.call_parser(lexer.lexerFromStream(
                Stream.streamFromString(string)))
        )
    string = "def fun(i){ var c = list(1,2); var j = [0, 1, 2]; return i; }"
    # string = repr(string)
    print(parse(string))


def test_parse28():
    def parse(string):
        return Parser.parse_expr(
            Parser.call_parser(lexer.lexerFromStream(
                Stream.streamFromString(string)))
        )
    string = "{var j = list(2, r);}"
    # string = repr(string)
    print(parse(string))


def test_parse29():
    def parse(string):
        return Parser.parse_expr(
            Parser.call_parser(lexer.lexerFromStream(
                Stream.streamFromString(string)))
        )
    string = "{ print p[a.length - 1];}"
    # string = repr(string)
    print(parse(string))


def test_parse30():
    def parse(string):
        return Parser.parse_expr(
            Parser.call_parser(lexer.lexerFromStream(
                Stream.streamFromString(string)))
        )
    string = "{ fun(a-1);}"
    # string = repr(string)
    print(parse(string))


def test_parse31():
    def parse(string):
        return Parser.parse_expr(
            Parser.call_parser(lexer.lexerFromStream(
                Stream.streamFromString(string)))
        )
    string = "{ a = fun(a+4, 0) + fun(b-9, 0);}"
    # string = repr(string)
    print(parse(string))


def test_parse32():
    def parse(string):
        return Parser.parse_expr(
            Parser.call_parser(lexer.lexerFromStream(
                Stream.streamFromString(string)))
        )
    string = "{ var a = {};}"
    # string = repr(string)
    print(parse(string))


def test_parse33():
    def parse(string):
        return Parser.parse_expr(
            Parser.call_parser(lexer.lexerFromStream(
                Stream.streamFromString(string)))
        )
    string = "{ a.iskey(3); }"
    # string = repr(string)
    print(parse(string))


def test_parse34():
    def parse(string):
        return Parser.parse_expr(
            Parser.call_parser(lexer.lexerFromStream(
                Stream.streamFromString(string)))
        )
    string = "{ dict[i] = i+1+4+9; }"
    # string = repr(string)
    print(parse(string))


def test_parse35():
    def parse(string):
        return Parser.parse_expr(
            Parser.call_parser(lexer.lexerFromStream(
                Stream.streamFromString(string)))
        )
    string = '{ a = "1" + "2"; }'
    # string = repr(string)
    print(parse(string))


def test_parse36():
    def parse(string):
        return Parser.parse_expr(
            Parser.call_parser(lexer.lexerFromStream(
                Stream.streamFromString(string)))
        )
    string = '{ a[7:2]; }'
    # string = repr(string)
    print(parse(string))


def test_parse37():
    def parse(string):
        return Parser.parse_expr(
            Parser.call_parser(lexer.lexerFromStream(
                Stream.streamFromString(string)))
        )
    string = '{ var a = input("string"); }'
    # string = repr(string)
    print(parse(string))

# test_parse0()
# test_parse1()
# test_parse2()
# test_parse3()
# test_parse4()
# test_parse5()
# test_parse6()
# test_parse7()
# test_parse8()
# test_parse9()
# test_parse10()
# test_parse11()
# test_parse12()
# test_parse13()
# test_parse14()
# test_parse15()
# test_parse16()
# test_parse17()
# test_parse18()
# test_parse19()
# test_parse20()
# test_parse21()
# test_parse22()
# test_parse23()
# test_parse24()
# test_parse28()
# test_parse29()
# test_parse30()
# test_parse31()
# test_parse34()
# test_parse36()
# test_parse37()
