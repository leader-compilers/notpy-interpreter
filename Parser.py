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
                return let_var(name)
            case Num(value):
                self.tokens.advance()
                return numeric_literal(value)
            case Bool(value):
                self.tokens.advance()
                return bool_literal(value)
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

    def parse_mult(self):
        left = self.parse_unary()
        while True:
            match self.tokens.peek_token():
                case Operator(op) if op in "*/":
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
            case Operator(op) if op == "&&" or op == "||":
                self.tokens.advance()
                right = self.parse_equal()
                return binary_operation(op, left, right)
        return left

    def parse_expr(self):
        match self.tokens.peek_token():
            case Keyword("if"):
                return self.parse_if()
            case Keyword("while"):
                return self.parse_while()
            case Keyword("print"):
                return self.parse_print()
            case _:
                return self.parse_logic()

    def parse_while(self):
        self.tokens.match(Keyword("while"))
        c = self.parse_expr()
        self.tokens.match(Keyword("do"))
        b = self.parse_expr()
        self.tokens.match(Keyword("end"))
        return while_loop(c, b)

    def parse_if(self):
        self.lexer.match(Keyword("if"))
        c = self.parse_expr()
        self.lexer.match(Keyword("then"))
        t = self.parse_expr()
        self.lexer.match(Keyword("else"))
        f = self.parse_expr()
        self.lexer.match(Keyword("end"))
        return if_statement(c, t, f)

    # for can be passed as while loop and some extra conditions
    def parse_for(self):
        self.lexer.match(Keyword("for"))
        iterator = self.parse_var()
        self.lexer.match(Operator(";"))
        condition = self.parse_expr()
        self.lexer.match(Operator(";"))
        increment = self.parse_expr()
        self.lexer.match(Keyword("do"))
        body = self.parse_expr()
        self.lexer.match(Keyword("end"))
        return for_loop(iterator, condition, increment, body)
    
    def parse_print(self):
        exprs = []
        while True:
            exprs.append(self.parse_expr())
            if not self.tokens.peek_token().matches(","):
                break
            self.tokens.match(",")
        return print_statement(exprs)

@dataclass
class NumType:
    pass


@dataclass
class BoolType:
    pass


SimType = NumType | BoolType

AST = numeric_literal | bool_literal | string_literal | binary_operation | let_var | unary_operation | while_loop | if_statement 

TypedAST = NewType('TypedAST', AST)


class TypeError(Exception):
    pass


def test_parse():
    def parse(string):
        return Parser.parse_expr(
            Parser.call_parser(lexer.lexerFromStream(
                Stream.streamFromString(string)))
        )

    # You should parse, evaluate and see whether the expression produces the expected value in your tests.
    print(parse("a+b^c*d+a+b-c+d+e*f/g"))


test_parse()  # Uncomment to see the created ASTs.
