import lexer as l
import Parser as p
import eval as e
import typechecking as t
import resolver as r
import bytecode as b


def main(filename):
    with open(filename) as f:
        code = f.read()
    code = '{' + code + '}'
    stream = l.Stream.streamFromString(code)
    tokens = l.lexer.lexerFromStream(stream)
    parse = p.Parser.call_parser(tokens)
    ast = p.Parser.parse_expr(parse)
    # print(ast)
    # resolvedast = r.resolve(ast)
    # print(resolvedast)
    # typedast = t.typecheck(resolvedast)
    output = e.eval_ast(ast)
    # v = b.VM()
    # v.load(b.compile(resolvedast))
    # # print(v.bytecode.insns)
    # output = v.execute()
    # print(output)


main("tester/eulertest.txt")
