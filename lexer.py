from dataclasses import dataclass
from typing import Union


class EndOfTokens(Exception):
    pass


class TokenError(Exception):
    pass


@dataclass
class Stream:
    source: str
    pos: int = 0

    def streamFromString(s):
        return Stream(s, 0)

    def next_char(self):
        if self.pos >= len(self.source):
            raise EndOfTokens()
        self.pos = self.pos + 1
        return self.source[self.pos - 1]

    def prev_char(self):
        assert self.pos > 0
        self.pos = self.pos - 1


# The different types of tokens


@dataclass
class Num:
    n: int


@dataclass
class Bool:
    b: bool


@dataclass
class Keyword:
    word: str


@dataclass
class Identifier:
    word: str


@dataclass
class String:
    s: str


@dataclass
class Operator:
    op: str


@dataclass
class EndOfLine:
    EOL: str


TokenType = Num | Bool | Keyword | Identifier | Operator | EndOfLine | String
keywords = "var true false print if else for while return end do Print".split()
operators = ", . ; + - * % > < >= <= == ! != ** ^".split()
word_operators = "and or not quot rem"
white_space = " \t\n"


@dataclass
class lexer:
    stream = None
    save: TokenType = None

    def lexerFromStream(s):
        self = lexer()
        self.stream = s
        return self

    def number(self, c: str) -> Num:
        n = int(c)
        while True:
            try:
                c = self.stream.next_char()
                if c.isdigit():
                    n = n * 10 + int(c)
                else:
                    self.stream.prev_char()
                    return Num(n)
            except EndOfTokens:
                return Num(n)

    def identifier(self, c: str) -> Identifier:
        word = c
        while True:
            try:
                c = self.stream.next_char()
                if c.isalpha():
                    word = word + c
                else:
                    self.stream.prev_char()
                    if word in keywords:
                        return Keyword(word)
                    else:
                        return Identifier(word)
            except EndOfTokens:
                if word in keywords:
                    return Keyword(word)
                else:
                    return Identifier(word)

    def string(self) -> String:
        s = ""
        while True:
            try:
                c = self.stream.next_char()
                if c == '"':
                    return String(s)
                else:
                    s = s + c
            except EndOfTokens:
                raise EndOfTokens()

    def next_token(self) -> TokenType:
        try:
            match self.stream.next_char():
                case c if c in operators:
                    return Operator(c)
                case c if c.isdigit():
                    return self.number(c)
                case c if c.isalpha():
                    return self.identifier(c)
                case c if c == '"':
                    return self.string()
                case c if c in white_space:
                    return self.next_token()
            # some elif statements are still to be done
        except EndOfTokens:
            raise EndOfTokens()

    def peek_token(self) -> TokenType:
        if self.save is not None:
            return self.save
        self.save = self.next_token()
        return self.save

    def advance(self):
        assert self.save is not None
        self.save = None

    def match(self, expected):
        if self.peek_token() == expected:
            return self.advance()
        raise TokenError()

    def __iter__(self):
        return self

    def __next__(self):
        try:
            return self.next_token()
        except EndOfTokens:
            raise StopIteration


def lexing_test1():
    s = Stream.streamFromString("if 22 >= 33 then 5+3 else 8*3 end;")
    l = lexer.lexerFromStream(s)
    for token in l:
        print(token)


def lexing_test2():
    s = Stream.streamFromString("var flag = True;")
    l = lexer.lexerFromStream(s)
    for token in l:
        print(token)


# lexing_test1()
# print("\n")
# lexing_test2()
