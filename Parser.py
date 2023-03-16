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
        # print(self.tokens.peek_token())
        match self.tokens.peek_token():
            case Identifier(name):
                self.tokens.advance()
                match self.tokens.peek_token():
                    case Operator(op) if op in "=":
                        self.tokens.advance()
                        return self.parse_set(name)
                    
                return get(identifier(name))
            case Num(value):
                self.tokens.advance()
                return numeric_literal(value)
            # case Bool(value):
            #     self.tokens.advance()
            #     return bool_literal(value)
            case String(value):
                self.tokens.advance()
                return string_literal(value)

    def parse_power(self):
        left = self.parse_primary()
        while True:

            match self.tokens.peek_token():
                case Operator(op) if op in "^":
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
                case Operator(op) if op in "!-":
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
            value = self.parse_expr()
            match self.tokens.peek_token():
                case Operator(op) if op in ";":
                    break
        if not value:
            return None
        return set(identifier(name), value)

                    
            

    def parse_expr(self):
        
        b = []
        match self.tokens.peek_token():
            case Operator(op) if op in "{":
                self.tokens.advance()
        while True:
            # print(self.tokens.peek_token())
            match self.tokens.peek_token():
                case Operator(op) if op in "{":
                    self.tokens.advance()

                case Operator(op) if op in "}":
                    self.tokens.advance()
                    return block(b)
                    break
                case EndOfLine(EOL) if EOL in "EndOfLine":
                    
                    return block(b)
                    break
                case Keyword("let"):
                    b.append(self.parse_let())
                    # return self.parse_let()
                    # return block(b)
                    match self.tokens.peek_token():
                        case Operator(op) if op in ";":
                            return block(b)
                case null("pass"):
                    b.append(self.parse_null())


                    # return self.parse_for()
                    # return block(b)
                    match self.tokens.peek_token():
                        case Operator(op) if op in ";":
                            return block(b)
                case Keyword("for"):
                    b.append(self.parse_for())

                    # return self.parse_for()
                    # return block(b)
                    match self.tokens.peek_token():
                        case Operator(op) if op in ";":
                            return block(b)
                case Keyword("for"):
                    b.append(self.parse_for())
                    # return self.parse_for()
                    # return block(b)
                    # print(self.tokens.peek_token())
                    # self.tokens.match(Operator(";"))
                case Keyword("if"):
                    b.append(self.parse_if())
                    # return self.parse_if()
                    match self.tokens.peek_token():
                        case Operator(op) if op in ";":
                            return block(b)
                case Keyword("def"):
                    # return self.parse_function()
                    b.append(self.parse_function())
                    # return block(b)
                    # print(self.tokens.peek_token())
                    self.tokens.match(Operator(";"))
                    
                case Keyword("while"):
                    b.append(self.parse_while())
                    # return self.parse_while()
                    # return block(b)
                    match self.tokens.peek_token():
                        case Operator(op) if op in ";":
                            return block(b)
                case Keyword("print"):
                    # print(self.tokens.peek_token())
                    b.append(self.parse_print())
                    # print(self.tokens.peek_token())
                    # return  self.parse_print()
                    # return block(b)
                    self.tokens.match(Operator(";"))
                case Keyword("List"):
                    b.append(self.parse_List())
                    # return self.parse_List()
                    # return block(b)
                    match self.tokens.peek_token():
                        case Operator(op) if op in ";":
                            return block(b)
                case Keyword("var"):
                    # print(self.tokens.peek_token(), "3")
                    b.append(self.parse_declare())

                    # print(b)
                    # return self.parse_declare()
                    
                    # match self.tokens.peek_token():
                    #     case Operator(op) if op in ";":
                    #         return block(b)
                    self.tokens.match(Operator(";"))
                    # self.tokens.match(Operator("}"))
                    # print(self.tokens.peek_token())
                case functionName(name):
                    # return self.parse_function_call()
                    b.append(self.parse_function_call())
                    # return self.parse_declare()
                    # print(self.tokens.peek_token())
                    self.tokens.match(Operator(";"))
                    # print(self.tokens.peek_token(), "1")
                case _:
                    tree = self.parse_logic()
                    return tree
                    
        return block(b)
    
    def parse_expr_func(self):
        
        b = []
        while True:
            
            match self.tokens.peek_token():
                case Operator(op) if op in "{":
                    self.tokens.advance()

                case Operator(op) if op in "}":
                    self.tokens.advance()
                    return block(b)
                    break
                case EndOfLine(EOL) if EOL in "EndOfLine":
                    
                    return block(b)
                    break
                case Keyword("let"):
                    b.append(self.parse_let())
                   
                    match self.tokens.peek_token():
                        case Operator(op) if op in ";":
                            return block(b)
                case null("pass"):
                    b.append(self.parse_null())
                    
                    match self.tokens.peek_token():
                        case Operator(op) if op in ";":
                            return block(b)
                case Keyword("for"):
                    b.append(self.parse_for())
                    
                    match self.tokens.peek_token():
                        case Operator(op) if op in ";":
                            return block(b)
                case Keyword("if"):
                    b.append(self.parse_if())
                    # return self.parse_if()
                    match self.tokens.peek_token():
                        case Operator(op) if op in ";":
                            return block(b)
                case Keyword("def"):
                    # return self.parse_function()
                    b.append(self.parse_function())
                    # return block(b)
                    # print(self.tokens.peek_token())
                    self.tokens.match(Operator(";"))
                    
                case Keyword("while"):
                    b.append(self.parse_while())
                    # return self.parse_while()
                    # return block(b)
                    match self.tokens.peek_token():
                        case Operator(op) if op in ";":
                            return block(b)

                case Keyword("print"):
                    
                    b.append(self.parse_print())
                    
                    self.tokens.match(Operator(";"))
                case Keyword("List"):
                    b.append(self.parse_List())
                    # return self.parse_List()

                case functionName(name):
                    return self.parse_function_call()
                case _:
                    tree = self.parse_set()
                    if tree == None:
                        tree = self.parse_logic()
                        # print(tree)
                        # print("i")
                        # print(tree)

                    # return block(b)
                    match self.tokens.peek_token():
                        case Operator(op) if op in ";":
                            return block(b)
                case Keyword("var"):
                    # print(self.tokens.peek_token(), "3")
                    b.append(self.parse_declare())
                    self.tokens.match(Operator(";"))
                    # self.tokens.match(Operator("}"))
                    # print(self.tokens.peek_token())
                case functionName(name):
                    # return self.parse_function_call()
                    b.append(self.parse_function_call())
                    # return self.parse_declare()
                    # print(self.tokens.peek_token())
                    self.tokens.match(Operator(";"))
                    # print(self.tokens.peek_token(), "1")
                case _:
                    b.append(self.parse_logic())
                    return b
                    
        return block(b)
    
    def parse_function_call(self):
        match self.tokens.peek_token():
            case functionName(name):
                self.tokens.advance()
                match self.tokens.peek_token():
                    case Operator("("):
                        self.tokens.advance()
                        parameters = []
                        while self.tokens.peek_token() is not None:

                            if isinstance(self.tokens.peek_token(), Identifier) or isinstance(self.tokens.peek_token(), Num) or isinstance(self.tokens.peek_token(), String):
                                if isinstance(self.tokens.peek_token(), Identifier):
                                    word = self.tokens.peek_token().word
                                    parameters.append(identifier(word))
                                elif isinstance(self.tokens.peek_token(), Num):
                                    word = self.tokens.peek_token().n
                                    parameters.append(numeric_literal(word))
                                elif isinstance(self.tokens.peek_token(), String):
                                    word = self.tokens.peek_token().s
                                    parameters.append(string_literal(word))
                                else:
                                    parameters.append(self.tokens.peek_token())
                                self.tokens.advance()
                                if isinstance(self.tokens.peek_token(), Operator) and self.tokens.peek_token().op == ")":
                                    self.tokens.advance()
                                    break
                                elif isinstance(self.tokens.peek_token(), Operator) and self.tokens.peek_token().op == ",":
                                    self.tokens.advance()
                                    continue
                                else:
                                    raise SyntaxError("Unexpected token")
                            elif isinstance(self.tokens.peek_token(), Operator) and self.tokens.peek_token().op == ";":
                                self.tokens.advance()
                                break
                            else:
                                raise SyntaxError("Unexpected token")
                        # self.tokens.match(Operator(";"))
                        return FunctionCall(identifier(name), parameters)

                    case _:
                        raise SyntaxError("Unexpected token")

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
                                        if isinstance(self.tokens.peek_token(), Identifier):
                                            word = self.tokens.peek_token().word
                                            parameters.append(identifier(word))
                                        elif isinstance(self.tokens.peek_token(), Num):
                                            word = self.tokens.peek_token().n
                                            parameters.append(numeric_literal(word))
                                        elif isinstance(self.tokens.peek_token(), String):
                                            word = self.tokens.peek_token().s
                                            parameters.append(string_literal(word))
                                        else:
                                            parameters.append(self.tokens.peek_token())
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
                                    # print(self.tokens.peek_token())
                                    exprs.append(self.parse_expr_func())
                                    match self.tokens.peek_token():
                                        case Keyword(word) if word in "return":
                                            self.tokens.advance()
                                            ret_expr = self.parse_expr()
                                            break

                                    self.tokens.match(Operator(";"))
                                body = []
                                bod = exprs[0]
                                
                                for i in bod: 
                                    
                                    if i == None:
                                        pass
                                    else:
                                        
                                        body.append(i)
                                    
                                

                                # print(self.tokens.peek_token())
                                self.tokens.match(Operator(";"))
                                self.tokens.match(Operator("}"))
                                
                                # print(self.tokens.peek_token())
                                return Function(identifier(name), parameters, block(body), ret_expr)

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
        c = self.parse_logic()
        self.tokens.match(Keyword("do"))
        # b = self.parse_expr()
        exprs = []
        while True:
            # if self.tokens.peek_token().matches(")"):
            #     break
            match self.tokens.peek_token():
                case Operator("}"):
                    self.tokens.advance()
                    break
            exprs.append(self.parse_expr())
            self.tokens.match(Operator(";"))
        b = block(exprs)
        self.tokens.match(Keyword("end"))
        self.tokens.match(Operator(";"))
        return while_loop(c, b)

    def parse_if(self):
        self.tokens.match(Keyword("if"))
        c = self.parse_logic()
        self.tokens.match(Keyword("then"))
        exprs = []
        while True:
            # if self.tokens.peek_token().matches(")"):
            #     break
            match self.tokens.peek_token():
                case Operator("}"):
                    self.tokens.advance()
                    break
            exprs.append(self.parse_expr())
            self.tokens.match(Operator(";"))
        t = block(exprs)
        self.tokens.match(Keyword("else"))
        exprs = []
        while True:
            # if self.tokens.peek_token().matches(")"):
            #     break
            match self.tokens.peek_token():
                case Operator("}"):
                    self.tokens.advance()
                    break
            exprs.append(self.parse_expr())
            self.tokens.match(Operator(";"))
        f = block(exprs)
        self.tokens.match(Keyword("end"))
        self.tokens.match(Operator(";"))
        return if_statement(c, t, f)

    # for can be passed as while loop and some extra conditions
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
        self.tokens.match(Operator(";"))
        self.tokens.match(Operator(")"))
        self.tokens.match(Keyword("do"))
        # body = self.parse_expr()
        exprs = []
        while True:
            # if self.tokens.peek_token().matches(")"):
            #     break
            match self.tokens.peek_token():
                case Operator(op) if op in "}":
                    self.tokens.advance()
                    break
            exprs.append(self.parse_expr())
            self.tokens.match(Operator(";"))
        body = block(exprs)
        self.tokens.match(Keyword("end"))
        self.tokens.match(Operator(";"))
        return for_loop(identifier(iterator), initial_value, condition, increment, body)

    def parse_print(self):
        self.tokens.match(Keyword("print"))
        # if self.tokens.peek_token().matches("("):
        #     self.tokens.advance()
        exprs = []
        while True:
            # if self.tokens.peek_token().matches(")"):
            #     break
            exprs.append(self.parse_expr())
            match self.tokens.peek_token():
                case Operator(op) if op in ";":
                    break
            self.tokens.match(Operator(","))
        # self.tokens.match(Operator(";"))
        return print_statement(exprs)

    def parse_List(self):
        self.tokens.match(Keyword("List"))
        values = []
        while True:
            values.append(self.parse_expr())
            match self.tokens.peek_token():
                case Operator(op) if op in ";":
                    break
            self.tokens.match(Operator(","))
        return Lists(values)

    def parse_let(self):
        self.tokens.match(Keyword("let"))
        name = self.tokens.peek_token()
        self.tokens.advance()
        self.tokens.match(Operator("="))
        value = self.parse_expr()
        self.tokens.match(Keyword("in"))
        body = self.parse_expr()
        self.tokens.match(Operator(";"))
        return let(name, value, body)

    def parse_declare(self):
        # print(self.tokens.peek_token(), "4")
        self.tokens.match(Keyword("var"))
        vari = self.tokens.peek_token().word
        self.tokens.advance()
        match self.tokens.peek_token():
            case Operator(op) if op != "=":
                return None
        self.tokens.advance()
        while True:
            # match self.tokens.peek_token():
            #     case Identifier(name):
            value = self.parse_expr()
            match self.tokens.peek_token():
                case Operator(op) if op in ";":
                    break
        if not value:
            return None
        # self.tokens.match(Operator(";"))
        return declare(identifier(vari), value)


def test_parse():
    def parse(string):
        return Parser.parse_expr(
            Parser.call_parser(lexer.lexerFromStream(
                Stream.streamFromString(string)))
        )

    # You should parse, evaluate and see whether the expression produces the expected value in your tests.
    # print("var total = 0; for( i = 1 ; i < 1001 ; i = i + 1; ) do {if 1 then {2;3;} else {3;} end;;} end;")
    print(parse("{var a =4; for( i = 1 ; i < 1001 ; i = i + 1; ) do {if i%3 == 0 or i%5==0 then {total = total + i;} else {total = total;} end;;} end;}"))

# test_parse()  # Uncomment to see the created ASTs.


def test_parse1():
    def parse(string):
        return Parser.parse_expr(
            Parser.call_parser(lexer.lexerFromStream(
                Stream.streamFromString(string)))
        )
    # print(parse("{print ans;}"))
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
    print(parse("{ 1or2 }"))
    print(eval_ast(parse("{1+2}"), None, None))


def test_parse4():
    def parse(string):
        return Parser.parse_expr(
            Parser.call_parser(lexer.lexerFromStream(
                Stream.streamFromString(string)))
        )

    # print(parse("a+b"))
    # You should parse, evaluate and see whether the expression produces the expected value in your tests.
    print(eval_ast(parse("{6+7+8;}")))


def test_parse5():
    def parse(string):
        return Parser.parse_expr(
            Parser.call_parser(lexer.lexerFromStream(
                Stream.streamFromString(string)))
        )

    # print(parse("var a = 2;"))
    # You should parse, evaluate and see whether the expression produces the expected value in your tests.
    # print(eval_ast(parse("var a = 2+3;;"),None, None))
    print(parse("{var a = 2+3; r = 2;}"))


def test_parse6():
    def parse(string):
        return Parser.parse_expr(
            Parser.call_parser(lexer.lexerFromStream(
                Stream.streamFromString(string)))
        )
    print(parse("{if 1 then {2;3;} else {3;} end;}"))


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
    print(parse("{def fun(n){var val = 2; return val;}; var t = {r(1);};}"))

def test_parse9():
    def parse(string):
        return Parser.parse_expr(
            Parser.call_parser(lexer.lexerFromStream(
                Stream.streamFromString(string)))
        )
    print(parse("fun(1); s = 1;"))


def test_parse10():
    def parse(string):
        return Parser.parse_expr(
            Parser.call_parser(lexer.lexerFromStream(
                Stream.streamFromString(string)))
        )
    print(parse("{while i<30 do {i=i+1;a=a+1;} end;}"))

def test_parse11():
    def parse(string):
        return Parser.parse_expr(
            Parser.call_parser(lexer.lexerFromStream(
                Stream.streamFromString(string)))
        )
    print(parse("{ pass; }"))
    # print(eval_ast(parse("{1+2}"), None, None))

# test_parse()
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
