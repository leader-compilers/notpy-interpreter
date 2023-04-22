import lexer as l
import Parser as p
import eval as e
import typechecking as t
import resolver as r
from bytecode import *
import time
def main(filename):
    with open(filename) as f:
        code = f.read()
    # code = '{' + code + '}'
    stream = l.Stream.streamFromString(code)
    tokens = l.lexer.lexerFromStream(stream)
    parse = p.Parser.call_parser(tokens)
    ast = p.Parser.parse_expr(parse)
    
    # resolvedast = r.resolve(ast)
    # print(ast)
    # v = VM()
    # v.load(compile(resolvedast))
    # print(v.bytecode.insns)
    # v.execute()
    print(ast)
    output = e.eval_ast(ast)
    end=time.time()
    print(end-start)

main("test.txt")
