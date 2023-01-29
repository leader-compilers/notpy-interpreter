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
            case _:
                return self.parse_logic()

@dataclass
class NumType:
    pass

@dataclass
class BoolType:
    pass

SimType = NumType | BoolType

AST = numeric_literal | bool_literal | binary_operation | let_var

TypedAST = NewType('TypedAST', AST)


class TypeError(Exception):
    pass


def test_parse():
    def parse(string):
        return Parser.parse_expr (
            Parser.call_parser(lexer.lexerFromStream(Stream.streamFromString(string)))
        )
    
    # You should parse, evaluate and see whether the expression produces the expected value in your tests.
    print(parse("a+b^c*d+a+b-c+d+e*f/g"))

test_parse() # Uncomment to see the created ASTs.