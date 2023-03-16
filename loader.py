import lexer as l
import Parser as p
import eval as e


def main(filename):
    with open(filename) as f:
        code = f.read()
    code = '{' + code + '}'
    stream = l.Stream.streamFromString(code)
    tokens = l.lexer.lexerFromStream(stream)
    parse = p.Parser.call_parser(tokens)
    ast = p.Parser.parse_expr(parse)
    output = e.eval_ast(ast)


if __name__ == "__main__":
    main("euler1.txt")
