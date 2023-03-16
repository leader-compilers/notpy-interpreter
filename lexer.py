from dataclasses import dataclass
from typing import Union


class EndOfTokens(Exception):
    pass


class EndOfStream(Exception):
    pass


class TokenError(Exception):
    def __init__(self, message, line, column):
        self.message = message
        self.line = line
        self.column = column

    def __str__(self):
        return f"{self.message} at line {self.line}, column {self.column}"


@dataclass
class Stream:
    source: str
    pos: int = 0
    line: int = 1
    column: int = 1

    @classmethod
    def streamFromString(cls, s):
        return cls(s, 0, 1, 1)

    def next_char(self) -> str:
        if self.pos >= len(self.source):
            raise EndOfTokens()

        c = self.source[self.pos]
        if c == "\n":
            self.line += 1
            self.column = 1
        else:
            self.column += 1

        self.pos += 1
        return c

    def prev_char(self):
        assert self.pos > 0
        self.pos -= 1
        c = self.source[self.pos]
        if c == "\n":
            self.line -= 1
            # Find the previous non-empty line and set the column accordingly
            for i in range(self.pos - 1, -1, -1):
                if self.source[i] == "\n":
                    break
                if not self.source[i].isspace():
                    self.column = self.pos - i
                    break
        else:
            self.column -= 1

# The different types of tokens


@dataclass
class Num:
    n: int


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


@dataclass
class functionName:
    name: str


@dataclass
class null:
    name: str


@dataclass
class boolValue:
    name: str


TokenType = Num | Keyword | Identifier | Operator | EndOfLine | String | functionName | null | boolValue
keywords = "pass def print var True False if else then for while return end do List let in".split()
operators = ", . ; + - * % > < / >= <= == ! != ** ^ ( ) [ ] = and or not } ;; {".split(
)
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
                if c.isalpha() or c == "_" or c.isdigit():
                    word = word + c
                elif c == "(":
                    self.stream.prev_char()
                    if word in keywords:
                        return Keyword(word)
                    return functionName(word)

                else:
                    self.stream.prev_char()
                    if word in keywords:
                        if word == "pass":
                            return null(word)
                        elif word == "True" or word == "False":
                            return boolValue(word)
                        else:
                            return Keyword(word)
                    elif word in operators:
                        return Operator(word)
                    else:
                        return Identifier(word)
            except EndOfTokens:
                if word in keywords:
                    if word == "pass":
                        return null(word)
                    elif word == "True" or word == "False":
                        return boolValue(word)
                    else:
                        return Keyword(word)
                elif word in operators:
                    return Operator(word)
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

    def operator(self, c: str) -> Operator:
        if c == "=":
            c = self.stream.next_char()
            if c == "=":
                return Operator("==")
            else:
                self.stream.prev_char()
                return Operator("=")
        elif c == "!":
            c = self.stream.next_char()
            if c == "=":
                return Operator("!=")
            else:
                self.stream.prev_char()
                return Operator("!")
        elif c == ">":
            c = self.stream.next_char()
            if c == "=":
                return Operator(">=")
            else:
                self.stream.prev_char()
                return Operator(">")
        elif c == "<":
            c = self.stream.next_char()
            if c == "=":
                return Operator("<=")
            else:
                self.stream.prev_char()
                return Operator("<")
        elif c == "&":
            c = self.stream.next_char()
            if c == "&":
                return Operator("and")
            else:
                self.stream.prev_char()
                return Operator("&")
        elif c == "|":
            c = self.stream.next_char()
            if c == "|":
                return Operator("or")
            else:
                self.stream.prev_char()
                return Operator("|")
        elif c == "^":
            c = self.stream.next_char()
            if c == "^":
                return Operator("**")
            else:
                self.stream.prev_char()
                return Operator("^")
        elif c == "/":
            c = self.stream.next_char()
            if c == "/":
                return Operator("//")
            else:
                self.stream.prev_char()
                return Operator("/")
        else:
            return Operator(c)

    def next_token(self) -> TokenType:
        try:
            c = self.stream.next_char()
            match c:
                case c if c in operators:
                    return self.operator(c)
                case c if c.isdigit():
                    return self.number(c)
                case c if c.isalpha() or c == "_":
                    return self.identifier(c)
                case c if c == '"':
                    return self.string()
                case c if c in white_space:
                    return self.next_token()

        except EndOfTokens:
            return EndOfLine("EndOfLine")
            #raise EndOfTokens()

        raise TokenError("Invalid token", self.stream.line, self.stream.column)

    #  will be used in lexing

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

# ifelse


def lexing_test1():
    try:
        s = Stream.streamFromString("if 22 >= 33 then 5+3 else 8*3 end;")
        l = lexer.lexerFromStream(s)
        for token in l:
            print(token)
    except TokenError as e:
        print(e)


# declaration
# print("\n")


def lexing_test2():
    try:
        s = Stream.streamFromString("var flag = true;")
        l = lexer.lexerFromStream(s)
        for token in l:
            print(token)
    except TokenError as e:
        print(e)

# for loop includes get, set, declare


# print("\n")


def lexing_test3():
    try:
        s = Stream.streamFromString(
            "for i = 1; i < 9; i = (i + 1) do b = (b + 5) end")
        l = lexer.lexerFromStream(s)
        for token in l:
            print(token)
    except TokenError as e:
        print(e)


# while loop

# print("\n")


def lexing_test4():
    try:
        s = Stream.streamFromString("while i < 9 do b = b + 5 end")
        l = lexer.lexerFromStream(s)
        for token in l:
            print(token)
    except TokenError as e:
        print(e)


# print("\n")


def lexing_test5():
    try:

        s = Stream.streamFromString("print 1, 2, 3")
        l = lexer.lexerFromStream(s)
        for token in l:
            print(token)
    except TokenError as e:
        print(e)


# print("\n")


def lexing_test6():
    try:
        s = Stream.streamFromString("List 1, 2, 3;")
        l = lexer.lexerFromStream(s)
        for token in l:
            print(token)
    except TokenError as e:
        print(e)


# print("\n")


def lexing_test7():
    try:
        s = Stream.streamFromString("print \"hello world\"")
        l = lexer.lexerFromStream(s)
        for token in l:
            print(token)
    except TokenError as e:
        print(e)


# print("\n")


def lexing_test8():
    try:
        s = Stream.streamFromString("let a = 1 in a + 1 end")
        l = lexer.lexerFromStream(s)
        for token in l:
            print(token)
    except TokenError as e:
        print(e)


def lexing_test9():
    try:
        s = Stream.streamFromString(
            "def 1dhairya_bhai_69(a, b){ return a + b; }")
        l = lexer.lexerFromStream(s)
        for token in l:
            print(token)
    except TokenError as e:
        print(e)


def lexing_test10():
    try:
        s = Stream.streamFromString(
            "def sumofsquares(n){val = n * (n + 1) * (2 * n + 1) / 6; return val;}")
        l = lexer.lexerFromStream(s)
        for token in l:
            print(token)
    except TokenError as e:
        print(e)


def lexing_test11():
    try:
        s = Stream.streamFromString(
            "{var total = False; for( i = 1 ; i < 1001 ; i = i + 1; ) do {if i%3 == 0 or i%5==0 then {total = total + i;} else {pass;} end;;} end;}")
        l = lexer.lexerFromStream(s)
        for token in l:
            print(token)
    except TokenError as e:
        print(e)

