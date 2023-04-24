import lexer as l
import Parser as p
import eval as e
import typechecking as t
import resolver as r
from bytecode import *


def main(filename):
    with open(filename) as f:
        code = f.read()
    code = '{' + code + '}'
    stream = l.Stream.streamFromString(code)
    tokens = l.lexer.lexerFromStream(stream)
    parse = p.Parser.call_parser(tokens)
    ast = p.Parser.parse_expr(parse)
    resolvedast = r.resolve(ast)
    #typedast = t.typecheck(resolvedast)
    #output = e.eval_ast(resolvedast)
    v = VM()
    v.load(compile(resolvedast))
    v.execute()


main("euler14.txt")
